import os
import tempfile
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QCheckBox, QMessageBox
from PyQt6.QtGui import QIcon

class PCCleaner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('C:\\Users\\Ali\\Documents\\GitHub\\WonderCleaner\\iconx.ico'))
        self.setWindowTitle("WonderCleaner | By YTAli")
        self.setGeometry(300, 200, 1000, 600)
        main_layout = QHBoxLayout()
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.scan_button = QPushButton("🔍 Start Scan")
        self.scan_button.clicked.connect(self.scan_files)
        left_layout.addWidget(self.scan_button)
        self.delete_button = QPushButton("🗑 Delete Selected Files")
        self.delete_button.clicked.connect(self.delete_selected)
        self.delete_button.setEnabled(False)
        left_layout.addWidget(self.delete_button)
        self.delete_all_button = QPushButton("🔥 Delete ALL!")
        self.delete_all_button.clicked.connect(self.delete_all)
        self.delete_all_button.setEnabled(False)
        left_layout.addWidget(self.delete_all_button)
        self.cleanup_options = {
            "Temp Files": tempfile.gettempdir(),
            "Windows Temp": "C:\\Windows\\Temp",
            "Windows Prefetch": "C:\\Windows\\Prefetch",
            "Windows Logs": "C:\\Windows\\Logs",
            "AppData Temp": os.path.expanduser("~") + "\\AppData\\Local\\Temp",
            "Chrome Cache": os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache"
        }
        self.checkboxes = []
        for key in self.cleanup_options:
            checkbox = QCheckBox(key)
            checkbox.setChecked(True)
            left_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        left_layout.addStretch()
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        right_layout.addWidget(self.file_list)
        self.status_label = QLabel("")
        right_layout.addWidget(self.status_label)
        main_layout.addWidget(left_panel, 3)
        main_layout.addWidget(right_panel, 7)
        self.setLayout(main_layout)
        self.files_to_delete = []
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-size: 14pt;
            }
            QPushButton {
                background-color: #e100ff;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14pt;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
            QCheckBox, QLabel {
                font-size: 14pt;
            }
            QListWidget{
                font-size: 10px;
            }
        """)

    def scan_files(self):
        self.file_list.clear()
        self.files_to_delete = []
        for checkbox, (label, path) in zip(self.checkboxes, self.cleanup_options.items()):
            if checkbox.isChecked() and os.path.exists(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.files_to_delete.append(file_path)
                        self.file_list.addItem(file_path)
        if self.files_to_delete:
            self.status_label.setText(f"✅ {len(self.files_to_delete)} files found.")
            self.delete_button.setEnabled(True)
            self.delete_all_button.setEnabled(True)
        else:
            self.status_label.setText("⚠ No unnecessary files found!")
            self.delete_button.setEnabled(False)
            self.delete_all_button.setEnabled(False)

    def delete_selected(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select at least one file to delete!")
            return
        confirm = QMessageBox.question(self, "Confirmation", "Do you really want to delete the selected files?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            deleted_count = 0
            failed_count = 0
            for item in selected_items:
                file_path = item.text()
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    self.file_list.takeItem(self.file_list.row(item))
                except Exception:
                    failed_count += 1
            self.status_label.setText(f"🗑 {deleted_count} files deleted | ❌ {failed_count} could not be deleted.")

    def delete_all(self):
        if not self.files_to_delete:
            QMessageBox.warning(self, "Nothing to Delete", "There are no files to delete!")
            return
        confirm = QMessageBox.question(self, "ARE YOU SURE?", "🔥 ALL found files will be deleted. Continue?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            deleted_count = 0
            failed_count = 0
            for file_path in self.files_to_delete:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception:
                    failed_count += 1
            self.file_list.clear()
            self.status_label.setText(f"🔥 {deleted_count} files deleted | ❌ {failed_count} could not be deleted.")
            self.delete_button.setEnabled(False)
            self.delete_all_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication([])
    window = PCCleaner()
    window.show()
    app.exec()
