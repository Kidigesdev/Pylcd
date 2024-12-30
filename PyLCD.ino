#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); // Passe die Adresse an (0x27 oder 0x3F)

void setup() {
  Serial.begin(9600); // Serielle Kommunikation starten
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Warte auf Daten...");
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // Empfange die Datenzeile
    if (data.length() > 0) {
      float cpu = 0;
      float used_ram = 0;
      float total_ram = 0;
      sscanf(data.c_str(), "%f, %f, %f", &cpu, &used_ram, &total_ram); // Daten parsen
      // Serielle rück übertragung zur bestätigung was empfangen wurde
      Serial.println(cpu);
      Serial.println(used_ram);
      Serial.println(total_ram);
      Serial.println(data);
      // LCD aktualisieren
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("CPU: "); lcd.print(cpu); lcd.print(" %");
      lcd.setCursor(0, 1);
      lcd.print("RAM: ");
      lcd.print(used_ram); lcd.print("/"); lcd.print(total_ram); lcd.print(" MB");
    }
  }
}
