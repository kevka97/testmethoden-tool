import streamlit as st

# Toggle für Dark/Light Mode
dark_mode = st.toggle("Dark Mode aktivieren")

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
st.markdown("<div class='subtitle'>Bestimmen Sie geeignete Testmethoden mit relevanten Tools und Fokus-Punkten.</div>", unsafe_allow_html=True)

# Eingabeformular für die Klassifikation
st.header("Systemklassifikation")
with st.form("classification_form"):
    system_name = st.text_input("Name des Systems/Services", value="")
    system_description = st.text_area("Kurzbeschreibung", value="")

    # Hauptkriterien mit "Bitte auswählen" als Standard
    system_type = st.selectbox("Systemtyp", ["Bitte auswählen", "Neuentwicklung", "Migration", "Update / Weiterentwicklung"], index=0)
    environment = st.selectbox("Betriebsumgebung", ["Bitte auswählen", "On-Premise", "Cloud"], index=0)
    real_time_processing = st.selectbox("Echtzeitverarbeitung erforderlich?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    data_sensitivity = st.selectbox("Datenart", ["Bitte auswählen", "Technische Logdaten", "Personenbezogene/Firmenkritische Daten"], index=0)
    regulatory_requirements = st.selectbox("Regulatorische Vorgaben?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    availability = st.selectbox("24/7 Verfügbarkeit erforderlich?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    high_api_dependence = st.selectbox("Hohe API-Abhängigkeit?", ["Bitte auswählen", "Ja", "Nein"], index=0)
    deployment_frequency = st.selectbox("Deployment-Frequenz", ["Bitte auswählen", "Monatlich", "Wöchentlich", "Täglich"], index=0)

    submit_button = st.form_submit_button("Empfohlene Testmethoden anzeigen")

# Verarbeitung der Eingaben und Ausgabe von Testmethoden mit Details
if submit_button:
    if "Bitte auswählen" in [system_type, environment, real_time_processing, data_sensitivity, regulatory_requirements, availability, high_api_dependence, deployment_frequency]:
        st.warning("Bitte füllen Sie alle Felder aus, bevor Sie Testmethoden anzeigen drücken.")
    else:
        st.subheader("Empfohlene Testmethoden für Ihr System")
        st.write(f"System-/Service-Name: {system_name}")
        st.write(f"Beschreibung: {system_description}")

        def display_test_method(name, description, tools, focus_points):
            """ Funktion zur formatierten Darstellung der Testmethoden """
            st.markdown(f"### {name}")
            st.write(f"Beschreibung: {description}")
            st.write(f"Erforderliche Tools: {', '.join(tools)}")
            st.write(f"Wichtige Fokus-Punkte: {', '.join(focus_points)}")
            st.markdown("---")

        # Falls Update / Weiterentwicklung gewählt wurde, zeige automatisch Regressionstests an
        if system_type == "Update / Weiterentwicklung":
            display_test_method(
                "Automatisierte Regressionstests",
                "Überprüfung, ob bestehende Funktionen nach einem Update weiterhin korrekt arbeiten.",
                ["Selenium", "Cypress", "JUnit"],
                ["Testautomatisierung", "Versionskontrolle", "Fehlervermeidung bei Updates"]
            )

        # Dynamische Empfehlungen mit Details für andere Systemtypen
        if system_type == "Migration":
            display_test_method(
                "Datenmigrationstests",
                "Überprüfung der Datenintegrität und -konsistenz nach der Migration.",
                ["Apache Nifi", "Talend", "dbForge Studio"],
                ["Vergleich von Quell- und Zieltabellen", "Automatisierte Validierung von Daten"]
            )

        if environment == "Cloud":
            display_test_method(
                "Performance- & Skalierbarkeitstests",
                "Bewertung der Systemleistung unter Lastbedingungen in der Cloud.",
                ["JMeter", "Gatling", "AWS Load Testing"],
                ["Auto-Scaling-Validierung", "Spitzenlast-Simulation"]
            )

        if real_time_processing == "Ja":
            display_test_method(
                "Performance-Tests",
                "Messung der Antwortzeiten und Durchsatzraten für Echtzeitanforderungen.",
                ["LoadRunner", "Locust", "K6"],
                ["Latenzoptimierung", "Stabilitätsprüfung unter Dauerlast"]
            )

        if data_sensitivity == "Personenbezogene/Firmenkritische Daten":
            display_test_method(
                "Security- und Compliance-Tests",
                "Überprüfung der Sicherheitsmechanismen und Konformität mit regulatorischen Vorgaben.",
                ["OWASP ZAP", "Burp Suite", "Qualys"],
                ["DSGVO-Konformität", "Penetrationstests"]
            )

        if regulatory_requirements == "Ja":
            display_test_method(
                "Regulatorische Tests",
                "Sicherstellung der Einhaltung gesetzlicher Anforderungen.",
                ["SonarQube", "Checkmarx", "Fortify"],
                ["ISO 27001-Konformität", "Automatisierte Code-Scans"]
            )

        if availability == "Ja":
            display_test_method(
                "Hochverfügbarkeitstests",
                "Tests zur Sicherstellung des unterbrechungsfreien Betriebs.",
                ["Chaos Monkey", "Gremlin", "Azure Resiliency Toolkit"],
                ["Failover-Tests", "Recovery-Zeit-Optimierung"]
            )

        if high_api_dependence == "Ja":
            display_test_method(
                "API-Tests",
                "Validierung der Funktionalität, Leistung und Sicherheit von APIs.",
                ["Postman", "RestAssured", "SoapUI"],
                ["Endpunkt-Verfügbarkeit", "Datenvalidierung"]
            )

        if deployment_frequency in ["Wöchentlich", "Täglich"]:
            display_test_method(
                "Automatisierte Regressionstests",
                "Sicherstellung, dass neue Deployments keine bestehenden Funktionen beeinträchtigen.",
                ["Selenium", "Cypress", "JUnit"],
                ["Testautomatisierung", "Versionskontrolle"]
            )
