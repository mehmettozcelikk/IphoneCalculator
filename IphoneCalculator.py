#Gerekli kütüphanelerin eklenmesi
from calculatorUI import Ui_MainWindow #calculatırUI ->PyQt5 Designer ile oluşturduğum arayüz
import sys
from PyQt5 import QtWidgets

#QMainWindow sınıfında miras alan sistemin çalışacağı sınıf
class Application(QtWidgets.QMainWindow):
    #Yapıcı metot
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.currentValue = 0.0  # Ekrandaki değer
        self.storedValue = None  # Önceki değer
        self.operator = None  # İşlem türü
        self.newInput = True  # Yeni giriş kontrolü

        # Sayı butonlarını bağlama işlemi (1,2,3..,9)
        self.connectNumberButtons()

        # Fonksiyonel butonları bağlanması
        self.ui.plusMinusSign.clicked.connect(self.toggleSign)
        self.ui.AC.clicked.connect(self.resetAll)
        self.ui.dot.clicked.connect(self.addDecimal)

        # Matematiksel işlem butonlarının bağlanması
        self.ui.plus.clicked.connect(lambda: self.setOperator("+"))
        self.ui.minus.clicked.connect(lambda: self.setOperator("-"))
        self.ui.times.clicked.connect(lambda: self.setOperator("*"))
        self.ui.div.clicked.connect(lambda: self.setOperator("/"))
        self.ui.mod.clicked.connect(lambda: self.setOperator("%"))
        self.ui.equal.clicked.connect(self.calculateRes)

    # Sayı butonlarını bağlama işleminin fonksiyonlaştırılması
    def connectNumberButtons(self):
        for button in [
            self.ui.zero, self.ui.one, self.ui.two, self.ui.three,
            self.ui.four, self.ui.five, self.ui.six, self.ui.seven,
            self.ui.eight, self.ui.nine
        ]:
            button.clicked.connect(self.enterNumber)

    #Girilen sayıyı sonuç ekranına yazdıran fonksiyon
    def enterNumber(self):
        button = self.sender()
        if self.newInput and self.ui.ResultScreen.text() not in ".":  # Yeni bir giriş yapılacaksa ve "." kullanılmamışsa ekran temizle
            self.ui.ResultScreen.setText(button.text())
            self.newInput = False
        else:
            self.ui.ResultScreen.setText(self.ui.ResultScreen.text() + button.text())

    # Sayının işaretini değiştiren fonksiyon (+/-)
    def toggleSign(self):
        value = float(self.ui.ResultScreen.text())
        if value != 0:
            self.ui.ResultScreen.setText(format(float(-value),".15g"))
        else:
            return

    #Hepsini temizle fonksiyonu (AC)
    def resetAll(self):
        self.ui.ResultScreen.setText("0")
        self.currentValue = 0.0
        self.storedValue = None
        self.operator = None
        self.newInput = True

    #Ondalık ekleme fonksiyonu (.)
    def addDecimal(self):
        if "." not in self.ui.ResultScreen.text():
            self.ui.ResultScreen.setText(self.ui.ResultScreen.text() + ".")

    #İşlem türünü alan fonksiyon 
    def setOperator(self, op):
        self.currentValue = float(self.ui.ResultScreen.text())
        self.operator = op
        self.newInput = True

    #Sonuç hesaplayan fonksiyon
    def calculateRes(self):
        if self.operator:  # İşlem tipi kontrol edilir
            secondValue = float(self.ui.ResultScreen.text())
            try:
                if self.operator == "+":
                    self.currentValue += secondValue
                elif self.operator == "-":
                    self.currentValue -= secondValue
                elif self.operator == "%":
                    self.currentValue %= secondValue
                elif self.operator == "*":
                    self.currentValue *= secondValue
                elif self.operator == "/":
                    if secondValue != 0:
                        self.currentValue /= secondValue
                    else:
                        raise ZeroDivisionError
                # Sonuç ekranı güncellenir
                self.ui.ResultScreen.setText(format(float(self.currentValue),'.15g'))
            except ZeroDivisionError:
                self.ui.ResultScreen.setText("Error")  # Sıfıra bölme hatası
                self.resetAll()
            finally:
                self.storedValue = None
                self.operator = None
                self.newInput = True

#Application sınıfından nesne üreten ve uygulamayı çalıştıran fonksiyon
def startApp():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())

startApp()
