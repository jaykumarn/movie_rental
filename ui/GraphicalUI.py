import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from domain.Errors import DuplicateException, InexistingException, AlreadyBurrowed


class MovieRentalGUI:
    def __init__(self, controller):
        self._ctrl = controller
        self._window = tk.Tk()
        self._window.title("Movie Rental Shop")
        self._window.geometry("1100x650")
        self._window.configure(bg="#2c3e50")
        
        self._setup_styles()
        self._create_widgets()
        
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2c3e50')
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Helvetica', 10))
        style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'), foreground='#ecf0f1')
        style.configure('TButton', font=('Helvetica', 9), padding=6)
        style.configure('Treeview', font=('Helvetica', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        style.configure('TLabelframe', background='#2c3e50')
        style.configure('TLabelframe.Label', background='#2c3e50', foreground='white', font=('Helvetica', 10, 'bold'))
        
    def _create_widgets(self):
        # Header
        header_frame = ttk.Frame(self._window)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = ttk.Label(header_frame, text="Movie Rental Shop Management", style='Title.TLabel')
        title_label.pack()
        
        # Main container
        main_frame = ttk.Frame(self._window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Left panel with scrollbar
        left_container = ttk.Frame(main_frame)
        left_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Canvas and scrollbar for left panel
        canvas = tk.Canvas(left_container, bg='#2c3e50', highlightthickness=0, width=280)
        scrollbar = ttk.Scrollbar(left_container, orient=tk.VERTICAL, command=canvas.yview)
        self._scrollable_frame = ttk.Frame(canvas)
        
        self._scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._create_action_panel(self._scrollable_frame)
        
        # Right panel - Data display
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._create_data_panel(right_panel)
        
    def _create_action_panel(self, parent):
        # Add DVD Section
        add_dvd_frame = ttk.LabelFrame(parent, text="Add New DVD", padding=10)
        add_dvd_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_dvd_frame, text="DVD ID:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self._new_dvd_id_entry = ttk.Entry(add_dvd_frame, width=18)
        self._new_dvd_id_entry.grid(row=0, column=1, pady=3, padx=(5, 0))
        
        ttk.Label(add_dvd_frame, text="DVD Name:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self._new_dvd_name_entry = ttk.Entry(add_dvd_frame, width=18)
        self._new_dvd_name_entry.grid(row=1, column=1, pady=3, padx=(5, 0))
        
        add_dvd_btn = ttk.Button(add_dvd_frame, text="Add DVD", command=self._add_dvd)
        add_dvd_btn.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)
        
        # Rent DVD Section
        rent_frame = ttk.LabelFrame(parent, text="Rent a DVD", padding=10)
        rent_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(rent_frame, text="DVD ID:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self._dvd_id_entry = ttk.Entry(rent_frame, width=18)
        self._dvd_id_entry.grid(row=0, column=1, pady=3, padx=(5, 0))
        
        ttk.Label(rent_frame, text="Client Name:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self._client_name_entry = ttk.Entry(rent_frame, width=18)
        self._client_name_entry.grid(row=1, column=1, pady=3, padx=(5, 0))
        
        ttk.Label(rent_frame, text="Rented Date:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self._rented_date_entry = ttk.Entry(rent_frame, width=18)
        self._rented_date_entry.grid(row=2, column=1, pady=3, padx=(5, 0))
        self._rented_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        ttk.Label(rent_frame, text="Return Date:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self._return_date_entry = ttk.Entry(rent_frame, width=18)
        self._return_date_entry.grid(row=3, column=1, pady=3, padx=(5, 0))
        default_return = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
        self._return_date_entry.insert(0, default_return)
        
        rent_btn = ttk.Button(rent_frame, text="Rent DVD", command=self._rent_dvd)
        rent_btn.grid(row=4, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)
        
        # Return DVD Section
        return_frame = ttk.LabelFrame(parent, text="Return a DVD", padding=10)
        return_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(return_frame, text="DVD ID:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self._return_dvd_id_entry = ttk.Entry(return_frame, width=18)
        self._return_dvd_id_entry.grid(row=0, column=1, pady=3, padx=(5, 0))
        
        return_btn = ttk.Button(return_frame, text="Return DVD", command=self._return_dvd)
        return_btn.grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)
        
        # Filter Section
        filter_frame = ttk.LabelFrame(parent, text="Search DVDs", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="DVD Name:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self._filter_entry = ttk.Entry(filter_frame, width=18)
        self._filter_entry.grid(row=0, column=1, pady=3, padx=(5, 0))
        
        filter_btn = ttk.Button(filter_frame, text="Search", command=self._filter_dvds)
        filter_btn.grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)
        
        # View buttons
        view_frame = ttk.LabelFrame(parent, text="View", padding=10)
        view_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(view_frame, text="Show All Rentals", command=self._show_rentals).pack(fill=tk.X, pady=3)
        ttk.Button(view_frame, text="Show All DVDs", command=self._show_all_dvds).pack(fill=tk.X, pady=3)
        
    def _create_data_panel(self, parent):
        columns = ('ID', 'Name/Title', 'Client', 'Rented Date', 'Return Date', 'Status')
        self._tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        self._tree.heading('ID', text='ID')
        self._tree.heading('Name/Title', text='Name/Title')
        self._tree.heading('Client', text='Client')
        self._tree.heading('Rented Date', text='Rented Date')
        self._tree.heading('Return Date', text='Return Date')
        self._tree.heading('Status', text='Status')
        
        self._tree.column('ID', width=50, anchor=tk.CENTER)
        self._tree.column('Name/Title', width=180)
        self._tree.column('Client', width=120)
        self._tree.column('Rented Date', width=130, anchor=tk.CENTER)
        self._tree.column('Return Date', width=130, anchor=tk.CENTER)
        self._tree.column('Status', width=80, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self._tree.yview)
        scrollbar_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self._tree.xview)
        self._tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self._tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Status bar
        self._status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self._window, textvariable=self._status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(0, 10))
        
    def _clear_tree(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
    
    def _add_dvd(self):
        dvd_id = self._new_dvd_id_entry.get().strip()
        dvd_name = self._new_dvd_name_entry.get().strip()
        
        if not dvd_id or not dvd_name:
            messagebox.showwarning("Input Error", "Please fill in both DVD ID and DVD Name")
            return
        
        try:
            dvd_id_int = int(dvd_id)
        except ValueError:
            messagebox.showerror("Input Error", "DVD ID must be a number")
            return
        
        try:
            self._ctrl.add_new_dvd(dvd_id_int, dvd_name)
            messagebox.showinfo("Success", f"DVD '{dvd_name}' added successfully")
            self._new_dvd_id_entry.delete(0, tk.END)
            self._new_dvd_name_entry.delete(0, tk.END)
            self._status_var.set(f"Added DVD: {dvd_name}")
            self._show_all_dvds()
        except DuplicateException as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def _rent_dvd(self):
        dvd_id = self._dvd_id_entry.get().strip()
        client_name = self._client_name_entry.get().strip()
        rented_date = self._rented_date_entry.get().strip()
        return_date = self._return_date_entry.get().strip()
        
        if not dvd_id or not client_name:
            messagebox.showwarning("Input Error", "Please fill in DVD ID and Client Name")
            return
        
        if not rented_date or not return_date:
            messagebox.showwarning("Input Error", "Please fill in Rented Date and Return Date")
            return
            
        try:
            self._ctrl.add_new_borrow(client_name, dvd_id, rented_date, return_date)
            messagebox.showinfo("Success", f"DVD {dvd_id} rented to {client_name}")
            self._dvd_id_entry.delete(0, tk.END)
            self._client_name_entry.delete(0, tk.END)
            self._rented_date_entry.delete(0, tk.END)
            self._return_date_entry.delete(0, tk.END)
            self._rented_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
            default_return = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
            self._return_date_entry.insert(0, default_return)
            self._status_var.set(f"Rented DVD {dvd_id} to {client_name}")
            self._show_rentals()
        except DuplicateException as e:
            messagebox.showerror("Error", str(e))
        except InexistingException as e:
            messagebox.showerror("Error", str(e))
        except AlreadyBurrowed as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def _return_dvd(self):
        dvd_id = self._return_dvd_id_entry.get().strip()
        
        if not dvd_id:
            messagebox.showwarning("Input Error", "Please enter the DVD ID to return")
            return
        
        try:
            borrows = self._ctrl._Controller__borepo.get_all()
            borrow_id = None
            for b in borrows:
                if str(b.get_id_dvd()) == dvd_id:
                    borrow_id = b.get_id()
                    break
            
            if borrow_id is None:
                messagebox.showerror("Error", "This DVD is not currently rented")
                return
                
            self._ctrl.delete_borrow(borrow_id)
            messagebox.showinfo("Success", f"DVD {dvd_id} returned successfully")
            self._return_dvd_id_entry.delete(0, tk.END)
            self._status_var.set(f"Returned DVD {dvd_id}")
            self._show_all_dvds()
        except InexistingException as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def _filter_dvds(self):
        filter_text = self._filter_entry.get().strip()
        
        if not filter_text:
            self._show_all_dvds()
            return
            
        self._clear_tree()
        dvds = self._ctrl.filter_dvds_name(filter_text)
        dvds_with_status = self._ctrl.get_dvds_with_status()
        status_map = {d['id']: d for d in dvds_with_status}
        
        if not dvds:
            self._status_var.set("No DVDs found matching the search criteria")
        else:
            for dvd in dvds:
                dvd_id = dvd.get_id_dvd()
                info = status_map.get(dvd_id, {})
                self._tree.insert('', tk.END, values=(
                    dvd_id,
                    dvd.get_name(),
                    info.get('client', ''),
                    info.get('rented_date', ''),
                    info.get('return_date', ''),
                    info.get('status', 'Available')
                ))
            self._status_var.set(f"Found {len(dvds)} DVD(s)")
            
    def _show_rentals(self):
        self._clear_tree()
        try:
            rentals = self._ctrl.list_rentals()
            if not rentals:
                self._status_var.set("No active rentals")
            else:
                for rental in rentals:
                    self._tree.insert('', tk.END, values=(
                        rental.get_id(),
                        rental.get_dvd_name(),
                        rental.get_client_name(),
                        rental.get_rented_date(),
                        rental.get_return_date(),
                        'Rented'
                    ))
                self._status_var.set(f"Showing {len(rentals)} rental(s)")
        except Exception as e:
            self._status_var.set(f"Error loading rentals: {str(e)}")
            
    def _show_all_dvds(self):
        self._clear_tree()
        try:
            dvds_with_status = self._ctrl.get_dvds_with_status()
            if not dvds_with_status:
                self._status_var.set("No DVDs in the system")
            else:
                for dvd in dvds_with_status:
                    self._tree.insert('', tk.END, values=(
                        dvd['id'],
                        dvd['name'],
                        dvd['client'],
                        dvd['rented_date'],
                        dvd['return_date'],
                        dvd['status']
                    ))
                self._status_var.set(f"Showing {len(dvds_with_status)} DVD(s)")
        except Exception as e:
            self._status_var.set(f"Error loading DVDs: {str(e)}")
    
    def run(self):
        self._show_all_dvds()
        self._window.mainloop()
