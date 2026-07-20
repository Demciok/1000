import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

class ExcelLogger:
    def __init__(self, file_name="fastest_wins.xlsx"):
        self.file_name = file_name
        
        # --- DEFINICJA1 STYLÓW (Konfiguracja wyglądu) ---
        self.font_header = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        self.font_data = Font(name="Segoe UI", size=10, color="1F2937")
        
        self.fill_header = PatternFill(start_color="065F46", end_color="065F46", fill_type="solid")
        self.fill_zebra = PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid")
        
        self.border_thin = Border(
            left=Side(style='thin', color='E5E7EB'),
            right=Side(style='thin', color='E5E7EB'),
            top=Side(style='thin', color='E5E7EB'),
            bottom=Side(style='thin', color='E5E7EB')
        )
        
        self.align_left = Alignment(horizontal="left", vertical="center")
        self.align_center = Alignment(horizontal="center", vertical="center")
        self.align_right = Alignment(horizontal="right", vertical="center")
        self.data_alignments = [self.align_left, self.align_center, self.align_right]

        # Automatyczna inicjalizacja pliku przy tworzeniu obiektu klasy
        self._initialize_file()

    def _initialize_file(self):
        """Metoda wewnętrzna: Tworzy plik i nagłówki, jeśli jeszcze nie istnieją."""
        if os.path.exists(self.file_name):
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Wyniki Gry"
        ws.views.sheetView[0].showGridLines = True  # Widoczne linie siatki

        # Dodanie nagłówków
        headers = ["Nazwa Gracza", "Liczba Rund", "Zdobyte Punkty"]
        ws.append([])  # Pusty wiersz odstępu
        ws.append(headers)

        # Stylizowanie nagłówków
        for col_idx in range(1, 4):
            cell = ws.cell(row=2, column=col_idx)
            cell.fill = self.fill_header
            cell.font = self.font_header
            cell.alignment = self.align_center
        
        ws.row_dimensions[2].height = 25
        wb.save(self.file_name)
        wb.close()

    def _stylize_row(self, ws, row_idx):
        """Metoda wewnętrzna: Stylizuje konkretny wiersz danych."""
        ws.row_dimensions[row_idx].height = 20

        for col_idx in range(1, 4):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = self.font_data
            cell.alignment = self.data_alignments[col_idx - 1]
            cell.border = self.border_thin
            
            # Formatowanie liczb całkowitych
            if col_idx in [2, 3]:
                cell.number_format = '#,##0'
                
            # Efekt naprzemiennych wierszy (zebra)
            if row_idx % 2 == 0:
                cell.fill = self.fill_zebra

    def _auto_fit_columns(self, ws):
        """Metoda wewnętrzna: Dopasowuje szerokość kolumn do zawartości."""
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
    
    def log_win(self, player_name, rounds, points):
        """Metoda publiczna: Zapisuje nowy wynik do pliku Excel."""
        wb = openpyxl.load_workbook(self.file_name)
        ws = wb.active
        
        # Dopisywanie danych
        ws.append([player_name, rounds, points])
        
        # Stylizacja i dopasowanie kolumn
        current_row = ws.max_row
        self._stylize_row(ws, current_row)
        self._auto_fit_columns(ws)
        
        wb.save(self.file_name)
        wb.close()