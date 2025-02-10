import streamlit as st

# CSS-Styling für die Anwendung
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f4f4;
        font-family: Arial, sans-serif;
    }
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #000000;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #333333;
        text-align: center;
        margin-bottom: 20px;
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
    system_name = st.text_input("Name des Systems/Services")
    system_description = st.text_area("Kurzbeschreibung")

    # Hauptkriterien
    system_type = st.selectbox("Systemtyp", ["Neuentwicklung", "Migration"])
    environment = st.selectbox("Betriebsumgebung", ["On-Premise", "Cloud"])
    real_time_processing = st.selectbox("Echtzeitverarbeitung erforderlich?", ["Ja", "Nein"])
    data_sensitivity = st.selectbox("Datenart", ["Technische Logdaten", "Personenbezogene/Firmenkritische Daten"])
    regulatory_requirements = st.selectbox("Regulatorische Vorgaben?", ["Ja", "Nein"])
    availability = st.selectbox("24/7 Verfügbarkeit erforderlich?", ["Ja", "Nein"])
    high_api_dependence = st.selectbox("Hohe API-Abhängigkeit?", ["Ja", "Nein"])
    deployment_frequency = st.selectbox("Deployment-Frequenz", ["Monatlich", "Wöchentlich", "Täglich"])

    submit_button = st.form_submit_button("Empfohlene Testmethoden anzeigen")

# Verarbeitung der Eingaben und Ausgabe von Testmethoden mit Details
if submit_button:
    st.subheader("Empfohlene Testmethoden für Ihr System")
    st.write(f"**System-/Service-Name:** {system_name}")
    st.write(f"**Beschreibung:** {system_description}")

    def display_test_method(name, description, tools, focus_points):
        """ Funktion zur formatierten Darstellung der Testmethoden """
        st.markdown(f"### {name}")
        st.write(f"**Beschreibung:** {description}")
        st.write(f"**Erforderliche Tools:** {', '.join(tools)}")
        st.write(f"**Wichtige Fokus-Punkte:** {', '.join(focus_points)}")
        st.markdown("---")

    # Dynamische Empfehlungen mit Details
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
