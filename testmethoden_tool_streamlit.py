import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

# Dark Mode Toggle (klein & sichtbar in der Kopfzeile)
col1, col2 = st.columns([6, 1])  # Hauptbereich + kleine Spalte für den Toggle
with col2:
    dark_mode = st.toggle("🌗")

# Falls test_recommendations noch nicht existiert, erstelle eine leere Liste davor:
test_recommendations = []  # Liste für den Excel-Export

# Styling für Dark & Light Mode
if dark_mode:
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: white;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Titel und Beschreibung
st.markdown("<div class='title'>Testmethoden-Empfehlungs-Tool</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Bestimmen Sie geeignete Testmethoden mit relevanten Tools und Best Practices.</div>", unsafe_allow_html=True)

# Eingabeformular für die Klassifikation
st.header("Systemklassifikation")
with st.form("classification_form"):
    system_name = st.text_input("Name des Systems/Services", value="")
    system_description = st.text_area("Kurzbeschreibung", value="")

    # Hauptkriterien mit "Bitte auswählen" als Standard
    system_type = st.selectbox("Systemtyp", ["Bitte auswählen", "Neuentwicklung", "Migration", "Update"], index=0)
    environment = st.selectbox("Betriebsumgebung", ["Bitte auswählen", "On-Premise", "Cloud"], index=0)
    real_time_processing = st.selectbox("Echtzeitverarbeitung erforderlich?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    data_sensitivity = st.selectbox("Datenart", ["Bitte auswählen", "Technische Logdaten", "Personenbezogene/Firmenkritische Daten"], index=0)
    regulatory_requirements = st.selectbox("Regulatorische Vorgaben?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    availability = st.selectbox("24/7 Verfügbarkeit erforderlich?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    high_api_dependence = st.selectbox("Hohe API-Abhängigkeit?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    deployment_frequency = st.selectbox("Deployment-Frequenz", ["Bitte auswählen", "Monatlich", "Wöchentlich", "Täglich"], index=0)

    submit_button = st.form_submit_button("Empfohlene Testmethoden anzeigen")

# Funktion zur strukturierten Anzeige der Testmethoden mit vollständigen Erklärungen
def display_test_method(name, description, problems, best_practices, tools):
    """ Formatiert die Testmethode mit ausführlicher Erklärung, Problemen und Best Practices """
    st.markdown(f"### {name}")
    st.write(f"**Beschreibung:** {description}")

    st.write("Häufige Probleme")
    for problem in problems:
        st.markdown(f"- {problem}")

    st.write("Best Practices")
    for practice in best_practices:
        st.markdown(f"- {practice}")

    st.write("Eingesetzte Tools")
    for tool_category, tool_list in tools.items():
        st.markdown(f"- **{tool_category}**: {', '.join(tool_list)}")

    st.markdown("---")

    # Speichert die Empfehlungen für den Export in Excel
    test_recommendations.append({
        "Testmethode": name,
        "Beschreibung": description,
        "Häufige Probleme": "\n".join(problems),
        "Best Practices": "\n".join(best_practices),
        "Eingesetzte Tools": "\n".join([f"{cat}: {', '.join(lst)}" for cat, lst in tools.items()])
    })

# Verarbeitung der Eingaben und Ausgabe von Testmethoden
if submit_button:
    if "Bitte auswählen" in [system_type, environment, real_time_processing, data_sensitivity, regulatory_requirements, availability, high_api_dependence, deployment_frequency]:
        st.warning("Bitte füllen Sie alle Felder aus, bevor Sie Testmethoden anzeigen.")
    else:
        st.subheader("Empfohlene Testmethoden für Ihr System")
        st.write(f"**System-/Service-Name:** {system_name}")
        st.write(f"**Beschreibung:** {system_description}")

        if system_type == "Migration":
            display_test_method(
                "Datenmigrationstests",
                "Sicherstellen, dass Daten während der Migration vollständig und korrekt übernommen werden.",
                ["Datenverluste oder unvollständige Übertragungen", "Formatierungsfehler oder inkonsistente Daten"],
                ["Vergleich von Quell- und Zieldaten", "Automatisierte Validierung nutzen"],
                {"Migrationstools": ["Talend", "dbForge Studio"]}
            )

        if system_type == "Update":
            display_test_method(
                "Regressionstests",
                "Sicherstellen, dass bestehende Funktionen nach einem Update noch korrekt arbeiten.",
                ["Funktionalitäten brechen nach Updates", "Performance-Probleme durch neue Änderungen"],
                ["Automatisierte Tests nutzen", "Schlüssel-Features priorisieren"],
                {"Regressionstests": ["Selenium", "Azure DevOps Pipelines"]}
            )

        if environment == "Cloud":
            display_test_method(
                "Performance-Tests",
                "Bewertung der Skalierbarkeit und Verfügbarkeit.",
                ["Lange Antwortzeiten unter Last", "Skalierungsprobleme bei wachsender Last"],
                ["Realistische Lasten simulieren", "Monitoring in die Tests integrieren"],
                {"Performance-Tests": ["JMeter", "Gatling"]}
            )

        display_test_method(
            "Explorative Tests",
            "Fehlersuche durch kreative, nicht vorher festgelegte Testszenarien.",
            ["Unerwartete Nutzereingaben führen zu Fehlern", "UI-Probleme, die automatisierte Tests nicht erfassen"],
            ["Unterschiedliche Benutzerrollen simulieren", "Tester dokumentieren spontane Fehler"],
            {"Explorative Testing": ["TestBuddy", "Session Tester"]}
        )

        display_test_method(
            "User Acceptance Tests (UAT)",
            "Sicherstellen, dass das System den Anforderungen der Endnutzer entspricht.",
            ["System erfüllt die Anforderungen der Nutzer nicht", "Unverständliche oder nicht intuitive Bedienung"],
            ["Echte Endnutzer einbinden", "Klar definierte Abnahmekriterien nutzen"],
            {"Dokumentation": ["Jira", "Confluence"]}
        )

        display_test_method(
            "End-to-End-Tests",
            "Sicherstellen, dass das gesamte System (Frontend, Backend, Datenbank) in einer realistischen Umgebung funktioniert.",
            ["Unstimmigkeiten zwischen Backend und Frontend", "Fehler durch Dateninkonsistenzen"],
            ["Tests unter produktionsnahen Bedingungen durchführen", "Komplexe Benutzerworkflows testen", "Automatisierung wo sinnvoll nutzen"],
            {"Testautomatisierung": ["Selenium", "Playwright", "Cypress"]}
        )
# Excel Export-Funktion
if test_recommendations:
    df = pd.DataFrame(test_recommendations)

    # Formatierte Excel-Datei erstellen
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Testmethoden", index=False)

        # Formatierung optimieren
        workbook = writer.book
        worksheet = writer.sheets["Testmethoden"]

        # Spaltenbreite automatisch anpassen
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_len)

    output.seek(0)

    # Download-Button für die Excel-Datei
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"Testmethoden_Empfehlung_{timestamp}.xlsx"

    st.download_button(
        label="📥 Empfehlungen als Excel herunterladen",
        data=output,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
