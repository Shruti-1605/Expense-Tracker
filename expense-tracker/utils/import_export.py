import csv
import json
import os
from datetime import datetime
from services.database import SessionLocal, Transaction
from tkinter import filedialog, messagebox
import shutil

class ImportExport:
    def __init__(self):
        self.db = SessionLocal()
    
    def export_to_csv(self, filename=None):
        """Export all transactions to CSV file"""
        try:
            if not filename:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Export Transactions to CSV"
                )
            
            if not filename:
                return False
            
            transactions = self.db.query(Transaction).all()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'date', 'amount', 'type', 'category', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for t in transactions:
                    writer.writerow({
                        'id': t.id,
                        'date': t.date,
                        'amount': t.amount,
                        'type': t.type,
                        'category': t.category or '',
                        'notes': t.notes or ''
                    })
            
            messagebox.showinfo("Success", f"Exported {len(transactions)} transactions to {filename}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
            return False
    
    def import_from_csv(self, filename=None):
        """Import transactions from CSV file"""
        try:
            if not filename:
                filename = filedialog.askopenfilename(
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Import Transactions from CSV"
                )
            
            if not filename:
                return False
            
            imported_count = 0
            
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    # Validate required fields
                    if not all(key in row for key in ['date', 'amount', 'type']):
                        continue
                    
                    try:
                        # Create new transaction
                        transaction = Transaction(
                            date=row['date'],
                            amount=float(row['amount']),
                            type=row['type'].lower(),
                            category=row.get('category', ''),
                            notes=row.get('notes', '')
                        )
                        
                        # Validate type
                        if transaction.type not in ['income', 'expense']:
                            continue
                        
                        self.db.add(transaction)
                        imported_count += 1
                        
                    except (ValueError, TypeError):
                        continue  # Skip invalid rows
                
                self.db.commit()
            
            messagebox.showinfo("Success", f"Imported {imported_count} transactions from CSV")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")
            return False
    
    def export_to_json(self, filename=None):
        """Export all transactions to JSON file"""
        try:
            if not filename:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                    title="Export Transactions to JSON"
                )
            
            if not filename:
                return False
            
            transactions = self.db.query(Transaction).all()
            
            data = {
                'export_date': datetime.now().isoformat(),
                'transactions': []
            }
            
            for t in transactions:
                data['transactions'].append({
                    'id': t.id,
                    'date': t.date,
                    'amount': t.amount,
                    'type': t.type,
                    'category': t.category,
                    'notes': t.notes
                })
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Exported {len(transactions)} transactions to JSON")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"JSON export failed: {str(e)}")
            return False
    
    def backup_database(self):
        """Create a backup of the database file"""
        try:
            backup_filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                title="Backup Database",
                initialname=f"expense_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )
            
            if not backup_filename:
                return False
            
            from config import DB_PATH
            shutil.copy2(DB_PATH, backup_filename)
            
            messagebox.showinfo("Success", f"Database backed up to {backup_filename}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            return False
    
    def restore_database(self):
        """Restore database from backup file"""
        try:
            backup_filename = filedialog.askopenfilename(
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                title="Restore Database from Backup"
            )
            
            if not backup_filename:
                return False
            
            # Confirm restore
            confirm = messagebox.askyesno(
                "Confirm Restore", 
                "This will replace all current data. Are you sure you want to restore from backup?"
            )
            
            if not confirm:
                return False
            
            from config import DB_PATH
            shutil.copy2(backup_filename, DB_PATH)
            
            messagebox.showinfo("Success", "Database restored successfully. Please restart the application.")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {str(e)}")
            return False