# Manual Testing Of Frontend

This repository contains the results of manual testing of the Frontend in the file `manualtests.md`.

## Structure of the `manualtests.md` File

The file documents the manual testing scenarios conducted for the Frontend, structured as follows:

### Testy Manualne Front-Endu

| Numer scenariusza | Opis scenariusza | Kroki testowe | Oczekiwany wynik | Wynik Testu |
|:------------------:|------------------|---------------|------------------|:-----------:|
| 1 | Użytkownik powinien móc wybrać uczelnie z głównej strony aplikacji | 1. Otwórz stronę główną aplikacji<br> 2. Wybierz uczelnie SGGW<br> 3. Kliknij przycisk "Pomiń" | Użytkownik widzi w okienku wyszukiwań tylko naukowców z uczelni SGGW | ✅ |
| 2 | Użytkownik powinien móc wybrać instytut z głównej strony aplikacji | 1. Otwórz stronę główną aplikacji<br> 2. Wybierz uczelnie SGGW<br> 3. Wybierz instytut "Institute of Agriculture" | Użytkownik widzi w okienku wyszukiwań tylko naukowców z instytutu "Institute of Agriculture" z uczelni SGGW | ✅ |
| 3 | Użytkownik powinien móc otworzyć profil naukowca w bazie uczelni | 1. Kliknij lewym przyciskiem myszy na zdjęcie naukowca w okienku wyszukiwań<br> 2. Kliknij w przycisk "Profil w bazie uczelni" | Użytkownik widzi profil danego naukowca na stronie bazy wiedzy uczelni | ✅ |
| ... | ... | ... | ... | ... |

Each row corresponds to a specific test scenario and contains the following columns:
1. **Numer scenariusza**: Unique identifier of the scenario.
2. **Opis scenariusza**: A brief description of the scenario's purpose.
3. **Kroki testowe**: Detailed steps for executing the test.
4. **Oczekiwany wynik**: The expected outcome upon successful execution.
5. **Wynik Testu**: The actual result of the test (`✅` for pass, `❌` for fail).

This structure ensures clarity and consistency in documenting the testing process. Each test scenario provides essential details for verifying functionality, ensuring the frontend's reliability and usability.
