from PySide.QtCore import *
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide.QtGui import *
import os
from model import Models
from model import Traveller
from starmap import MapGlyphs
from starmap import MapGrid
from log import *

TITLE_FONT = 14
BODY_FONT = 10


class StatisticsDialog(QDialog):
    def __init__(self, pmi_list, numcells, name, parent=None):
        super(StatisticsDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Statistics Report')

        self.report = StatisticsReport(pmi_list, numcells, name)

        editor = QTextEdit()
        editor.setDocument(self.report.document)

        self.pdfButton = QPushButton('Save As PDF')
        self.closeButton = QPushButton('Close')

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.pdfButton)
        buttonLayout.addWidget(self.closeButton)
        buttonLayout.addStretch()

        layout = QHBoxLayout()
        layout.addWidget(editor)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        #self.connect(pdfButton, SIGNAL("clicked()"),
        #             self.exportToPdf)
        self.pdfButton.clicked.connect(self.exportToPdf)
        
        #self.connect(closeButton, SIGNAL("clicked()"),
        #             self.closeButtonClicked)
        self.closeButton.clicked.connect(self.closeButtonClicked)
        
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)


    def exportToPdf(self):
        #filename = 'World report.pdf'
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPaperSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        default_path = os.path.join(self.report.model.project_path,
                                    'StatisticsReport')
        filename = QFileDialog.getSaveFileName(self, 'Save as PDF',
                                               default_path,
                                               'PDF Files (*.pdf)')
        printer.setOutputFileName(filename)
        self.report.document.print_(printer)


    def closeButtonClicked(self):
        self.close()


class StatisticsReport(object):
    def __init__(self, pmi_list, numcells, name):
        if len(pmi_list) == 0:
            self.document = QTextDocument()
            cursor = QTextCursor(self.document)
            body_text_format = QTextCharFormat()
            body_text_format.setFont(QFont('Helvetica',
                                          BODY_FONT,
                                          QFont.Normal))
            body_block_format = QTextBlockFormat()
            body_block_format.setAlignment(Qt.AlignTop)
            body_block_format.setBottomMargin(0)
            body_block_format.setIndent(1)

            cursor.insertBlock()
            cursor.setBlockFormat(body_block_format)
            cursor.insertText('No worlds in selected area', body_text_format)

        else:
            
            self.model = pmi_list[0].model()

            world_list = []
            starport_list = [0] * 6
            size_list = [0] * 11
            atmo_list = [0] * 16
            hydro_list = [0] * 11
            pop_list = [0]* 13
            gov_list = [0] * 14
            law_list = [0] * 10
            tech_list = [0] * 24
            tech_max = 0
            total_pop = 0

            Ag = 0; As = 0; Ba = 0; De = 0; Fl = 0; Ga = 0; Hi = 0; Ht = 0; IC = 0
            In = 0; Lo = 0; Lt = 0; Na = 0; NI = 0; Po = 0; Ri = 0; Va = 0; Wa = 0
            
            for pmi in pmi_list:
                w = self.model.getWorld(pmi)
                world_list.append(w)
                starport_list[w.starport.index] += 1
                size_list[w.size.index] += 1
                atmo_list[w.atmosphere.index] +=1
                hydro_list[w.hydrographics.index] += 1
                pop_list[w.population.index] += 1
                total_pop += w.population.inhabitants
                gov_list[w.government.index] += 1
                law_list[w.lawLevel.index] += 1
                tech_list[w.techLevel.index] += 1
                if w.techLevel.index > tech_max: tech_max = w.techLevel.index

                if w.tradeAg: Ag += 1
                if w.tradeAs: As += 1
                if w.tradeBa: Ba += 1
                if w.tradeDe: De += 1
                if w.tradeFl: Fl += 1
                if w.tradeGa: Ga += 1
                if w.tradeHi: Hi += 1
                if w.tradeHt: Ht += 1
                if w.tradeIC: IC += 1
                if w.tradeIn: In += 1
                if w.tradeLo: Lo += 1
                if w.tradeLt: Lt += 1
                if w.tradeNa: Na += 1
                if w.tradeNI: NI += 1
                if w.tradePo: Po += 1
                if w.tradeRi: Ri += 1
                if w.tradeVa: Va += 1
                if w.tradeWa: Wa += 1

            col_max = 16
            if tech_max > col_max: col_max = tech_max
            world_number = len(world_list)
            
            self.document = QTextDocument()
            cursor = QTextCursor(self.document)

            title_text_format = QTextCharFormat()
            title_text_format.setFont(QFont('Helvetica',
                                            TITLE_FONT,
                                            QFont.Bold))
            title_block_format = QTextBlockFormat()
            title_block_format.setTopMargin(TITLE_FONT)

            bold_text_format = QTextCharFormat()
            bold_text_format.setFont(QFont('Helvetica',
                                          BODY_FONT,
                                          QFont.Bold))
            body_text_format = QTextCharFormat()
            body_text_format.setFont(QFont('Helvetica',
                                          BODY_FONT,
                                          QFont.Normal))
            body_block_format = QTextBlockFormat()
            body_block_format.setAlignment(Qt.AlignTop)
            body_block_format.setBottomMargin(0)
            body_block_format.setIndent(1)

    ##        table_constraints = [QTextLength(QTextLength.PercentageLength, 25),
    ##                             QTextLength(QTextLength.PercentageLength, 30),
    ##                             QTextLength(QTextLength.PercentageLength, 25),
    ##                             QTextLength(QTextLength.PercentageLength, 20)]
            form_table_format = QTextTableFormat()
            form_table_format.setCellSpacing(0)
            form_table_format.setCellPadding(3)
            form_table_format.setBorderBrush(QBrush(Qt.transparent))

            attrib_table_format = QTextTableFormat()
            attrib_table_format.setCellSpacing(0)
            attrib_table_format.setCellPadding(3)
            attrib_table_format.setBorderBrush(QBrush(Qt.transparent))
    ##        form_table_format.setColumnWidthConstraints(table_constraints)

            details_table_format = QTextTableFormat()
            details_table_format.setCellSpacing(0)
            details_table_format.setCellPadding(7)
            details_table_format.setBorderBrush(QBrush(Qt.transparent))

            cursor.insertBlock()
            cursor.setBlockFormat(title_block_format)
            cursor.insertText('Summary', title_text_format)

            summary_table = cursor.insertTable(4, 2, form_table_format)
            cell = summary_table.cellAt(0, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Number of Hexes: ', body_text_format)
            cell = summary_table.cellAt(0, 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(str(numcells), body_text_format)

            cell = summary_table.cellAt(1, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Number of Worlds: ', body_text_format)
            cell = summary_table.cellAt(1, 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(str(world_number), body_text_format)

            cell = summary_table.cellAt(2, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('World Occurrence: ', body_text_format)
            cell = summary_table.cellAt(2, 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(str(int((world_number * 100) / numcells)) + '%', body_text_format)

            def splitThousands(s, sep=','):
                        if len(s) <= 3: return s
                        return splitThousands(s[:-3], sep) + sep + s[-3:]
            cell = summary_table.cellAt(3, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Total Inhabitants: ', body_text_format)
            cell = summary_table.cellAt(3, 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(splitThousands(str(total_pop)), body_text_format)

            cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)

            cursor.insertBlock()
            cursor.setBlockFormat(title_block_format)
            cursor.insertText('World Attributes', title_text_format)

            table_constraints = [QTextLength(QTextLength.PercentageLength, 15)]
            colwidth = int(85 / col_max)
            for col in range(col_max):
                table_constraints.append(QTextLength(QTextLength.PercentageLength, colwidth))
            attrib_table_format.setColumnWidthConstraints(table_constraints)

            main_table = cursor.insertTable(9, col_max + 2, attrib_table_format)
            cell = main_table.cellAt(0, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Starport', body_text_format)
            for column in range(len(Traveller.starport_types)):
                port_type = Traveller.starport_types[column]
                total = str(starport_list[column])
                cell = main_table.cellAt(0, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(port_type + ':' + total, body_text_format)
            
            cell = main_table.cellAt(1, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Attribute', bold_text_format)
            for column in range(col_max):
                col_label = str(Traveller.tech_level_types[column])
                cell = main_table.cellAt(1, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(col_label, bold_text_format)

            cell = main_table.cellAt(2, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Size', body_text_format)
            for column in range(len(Traveller.size_types)):
                if size_list[column] == 0:
                    total = ''
                else:
                    total = str(size_list[column])
                cell = main_table.cellAt(2, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(total, body_text_format)

            cell = main_table.cellAt(3, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Atmosphere', body_text_format)
            for column in range(len(Traveller.atmosphere_types)):
                if atmo_list[column] == 0:
                    total = ''
                else:
                    total = str(atmo_list[column])
                cell = main_table.cellAt(3, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(total, body_text_format)

            cell = main_table.cellAt(4, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Hydrographics', body_text_format)
            for column in range(len(Traveller.hydrographics_types)):
                if hydro_list[column] == 0:
                    total = ''
                else:
                    total = str(hydro_list[column])
                cell = main_table.cellAt(4, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(total, body_text_format)

            cell = main_table.cellAt(5, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Population', body_text_format)
            for column in range(len(Traveller.population_types)):
                if pop_list[column] == 0:
                    total = ''
                else:
                    total = str(pop_list[column])
                cell = main_table.cellAt(5, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(total, body_text_format)

            cell = main_table.cellAt(6, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Government', body_text_format)
            for column in range(len(Traveller.government_types)):
                if gov_list[column] == 0:
                    total = ''
                else:
                    total = str(gov_list[column])
                cell = main_table.cellAt(6, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(total, body_text_format)

            cell = main_table.cellAt(7, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Law Level', body_text_format)
            for column in range(len(Traveller.law_level_types)):
                if law_list[column] == 0:
                    total = ''
                else:
                    total = str(law_list[column])
                cell = main_table.cellAt(7, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(total, body_text_format)

            cell = main_table.cellAt(8, 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText('Tech Level', body_text_format)
            for column in range(col_max):
                if tech_list[column] == 0:
                    total = ''
                else:
                    total = str(tech_list[column])
                cell = main_table.cellAt(8, column + 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(total, body_text_format)

            cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)

            cursor.insertBlock()
            cursor.setBlockFormat(title_block_format)
            cursor.insertText('Trade Code Frequency', title_text_format)


            trade_table = cursor.insertTable(19, 2, form_table_format)
            count = 0
            for row in (('Trade Code', 'Worlds'),
                        ('Agricultural', str(Ag)),
                        ('Asteroid', str(As)),
                        ('Barren', str(Ba)),
                        ('Desert', str(De)),
                        ('Fluid Oceans', str(Fl)),
                        ('Garden', str(Ga)),
                        ('High Population', str(Hi)),
                        ('High Technology', str(Ht)),
                        ('Ice-Capped', str(IC)),
                        ('Industrial', str(In)),
                        ('Low Population', str(Lo)),
                        ('Low Technology', str(Lt)),
                        ('Non-Agricultural', str(Na)),
                        ('Non-Industrial', str(NI)),
                        ('Poor', str(Po)),
                        ('Rich', str(Ri)),
                        ('Vacuum', str(Va)),
                        ('Water World', str(Wa))):
                cell = trade_table.cellAt(count, 0)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(row[0], body_text_format)
                cell = trade_table.cellAt(count, 1)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(row[1], body_text_format)
                count += 1

            cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        
        

        

        
