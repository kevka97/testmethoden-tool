import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

# Audi-Logo einfügen (Logo-Datei muss im selben Ordner liegen)
st.image("audi_logo.png", width=150)

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

    system_description = st.text_area(
        "Kurzbeschreibung ",
        value="",
        help="Beschreiben Sie das System oder den Service kurz und prägnant."
    )

    system_type = st.selectbox(
        "Systemtyp ",
        ["Bitte auswählen", "Neuentwicklung", "Migration", "Update"],
        index=0,
        help="Wählen Sie aus, ob das System neu entwickelt wird, eine Migration erfolgt oder ein Update durchgeführt wird."
    )

    environment = st.selectbox(
        "Betriebsumgebung ",
        ["Bitte auswählen", "On-Premise", "Cloud"],
        index=0,
        help="On-Premise bedeutet, dass das System lokal gehostet wird. Cloud bedeutet, dass das System in einer Cloud-Umgebung betrieben wird."
    )

    real_time_processing = st.selectbox(
        "Echtzeitverarbeitung erforderlich? ",
        ["Bitte auswählen", "Ja", "Nein"],
        index=0,
        help="Benötigt Ihr System eine sofortige Verarbeitung von Daten, ohne Verzögerung?"
    )

    data_sensitivity = st.selectbox(
        "Datenart ",
        ["Bitte auswählen", "Technische Logdaten", "Personenbezogene/Firmenkritische Daten"],
        index=0,
        help="Handelt es sich um einfache technische Logs oder um personenbezogene bzw. firmenkritische Daten, die besonders geschützt werden müssen?"
    )

    regulatory_requirements = st.selectbox(
        "Regulatorische Vorgaben? ",
        ["Bitte auswählen", "Ja", "Nein"],
        index=0,
        help="Gibt es gesetzliche oder branchenspezifische Vorschriften (z. B. DSGVO, ISO 27001), die Ihr System einhalten muss?"
    )

    availability = st.selectbox(
        "24/7 Verfügbarkeit erforderlich? ",
        ["Bitte auswählen", "Ja", "Nein"],
        index=0,
        help="Muss Ihr System rund um die Uhr verfügbar sein, ohne geplante Ausfälle?"
    )

    high_api_dependence = st.selectbox(
        "Hohe API-Abhängigkeit? ",
        ["Bitte auswählen", "Ja", "Nein"],
        index=0,
        help="Ist Ihr System stark auf externe oder interne APIs angewiesen?"
    )

    deployment_frequency = st.selectbox(
        "Deployment-Frequenz ",
        ["Bitte auswählen", "Monatlich", "Wöchentlich", "Täglich"],
        index=0,
        help="Wie oft werden neue Versionen des Systems bereitgestellt? Dies beeinflusst die Notwendigkeit für automatisierte Tests."
    )

    submit_button = st.form_submit_button("Empfohlene Testmethoden anzeigen")

# Funktion zur strukturierten Anzeige der Testmethoden mit vollständigen Erklärungen
def display_test_method(name, description, problems, best_practices, tools):
    """ Formatiert die Testmethode mit ausführlicher Erklärung, Problemen und Best Practices """
    st.markdown(f"### {name}")
    st.write(f"**Beschreibung:** {description}")

    st.write("Häufige Probleme:")
    for problem in problems:
        st.markdown(f"- {problem}")

    st.write("Best Practices:")
    for practice in best_practices:
        st.markdown(f"- {practice}")

    st.write("Eingesetzte Tools:")
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
    if "Bitte auswählen" in [system_type, environment, real_time_processing, data_sensitivity, regulatory_requirements,
                             availability, high_api_dependence, deployment_frequency]:
        st.warning("Bitte füllen Sie alle Felder aus, bevor Sie Testmethoden anzeigen.")
    else:
        st.subheader("Empfohlene Testmethoden für Ihr System")
        st.write(f"**System-/Service-Name:** {system_name}")
        st.write(f"**Beschreibung:** {system_description}")

        # Füge hier den Trennstrich hinzu, bevor die Empfehlungen starten
        st.markdown("---")

        # SYSTEMTYP
        if system_type == "Migration":
            display_test_method(
                "Datenmigrationstests",
                "Datenmigrationstests stellen sicher, dass alle Daten aus dem Quellsystem vollständig, "
                "korrekt und ohne Datenverlust oder -korruption in das Zielsystem übertragen werden. "
                "Dies ist besonders wichtig, um die Datenintegrität und Konsistenz nach der Migration zu gewährleisten.",
                ["Datenverluste oder unvollständige Übertragungen, die durch fehlerhafte Extraktions-, Transformations- oder Ladeprozesse (ETL) entstehen können.",
                "Formatierungsfehler oder inkonsistente Daten aufgrund unterschiedlicher Datenstrukturen oder inkompatibler Zeichensätze zwischen Quell- und Zielsystem.",
                "Verlust von Beziehungen oder Abhängigkeiten zwischen Datensätzen, insbesondere bei relationalen Datenbanken.",
                "Performanzprobleme während der Migration, die zu Zeitüberschreitungen oder Systemausfällen führen können."],
                ["Vergleich von Quell- und Zieldaten durch Hash-Prüfsummen oder Row-Count-Validierungen zur Identifikation von Differenzen.",
                "Einsatz automatisierter Validierungswerkzeuge zur Überprüfung von Datenintegrität und -konsistenz.",
                "Stichprobenbasierte manuelle Prüfung kritischer Datensätze zur Sicherstellung der erwarteten Datenqualität.",
                "Einsatz von Testmigrationen in einer isolierten Umgebung, um potenzielle Probleme vor der Produktivmigration zu identifizieren.",
                "Durchführung von Performanztests zur Bewertung der Migrationseffizienz und zur Identifikation von Engpässen."],
                {"Migrationstools": ["Talend", "dbForge Studio"]}
            )

        if system_type == "Update":
            display_test_method(
                "Regressionstests",
                "Regressionstests stellen sicher, dass nach einer Änderung oder einem Update bestehende "
                "Funktionen weiterhin korrekt arbeiten, ohne dass unerwartete Fehler auftreten. "
                "Diese Tests sind besonders wichtig in agilen Entwicklungsprozessen mit häufigen Releases, um die "
                "Stabilität der Anwendung sicherzustellen.",
                ["Funktionalitäten brechen nach Updates, insbesondere wenn Abhängigkeiten zwischen Modulen nicht ausreichend getestet wurden.",
                "Performance-Probleme durch neue Änderungen, die unerwartete Lastspitzen oder Engpässe verursachen.",
                "Nicht-erfasste Seiteneffekte in bestehenden Workflows, die zu unerwartetem Verhalten führen können.",
                "Fehlende Abdeckung von kritischen Geschäftsprozessen, was zu Produktionsausfällen führen kann."],
                ["Automatisierte Regressionstests in den CI/CD-Prozess integrieren, um frühzeitige Fehlererkennung zu ermöglichen.",
                 "Schlüssel-Features priorisieren und sicherstellen, dass Kernfunktionalitäten nach jedem Update getestet werden.",
                 "Smoke-Tests als ersten Schritt ausführen, um grundlegende Funktionen schnell zu überprüfen.",
                 "Differenzielle Tests verwenden, um nur die direkt betroffenen Bereiche effizient zu testen.",
                 "Regelmäßige Code-Reviews und statische Code-Analysen ergänzend zu Regressionstests einsetzen."],
                {"Regressionstests": ["Selenium", "Azure DevOps Pipelines"]}
            )

        # ECHTZEITVERARBEITUNG
        if real_time_processing == "Ja" and environment == "Cloud":
            display_test_method(
                "Disaster Recovery Tests",
                "Disaster Recovery Tests überprüfen, ob ein System nach unerwarteten Ausfällen schnell und "
                "zuverlässig wiederhergestellt werden kann.Dies ist besonders im Cloud-Umfeld relevant, wo hochverfügbare "
                "und skalierbare Architekturen genutzt werden, aber dennoch Ausfälle durch Fehlkonfigurationen, Datenverlust "
                "oder externe Angriffe auftreten können.",
                ["Datenverluste oder lange Wiederherstellungszeiten durch unzureichende oder fehlerhafte Backup- und Wiederherstellungsstrategien.",
                "Fehlendes automatisiertes Backup, wodurch Daten in Echtzeit verloren gehen können, insbesondere bei Datenbank-Clustern oder Streaming-Diensten.",
                "Netzwerk- oder Infrastruktur-Ausfälle in Cloud-Umgebungen, die zu Systemausfällen oder Latenzproblemen führen.",
                "Unzureichende Failover-Mechanismen, die nicht automatisiert ausgelöst werden und manuelle Eingriffe erfordern."],
                ["Regelmäßige Backup- & Restore-Tests durchführen, um die Integrität und Konsistenz der Backups zu gewährleisten.",
                "Disaster-Recovery-Pläne dokumentieren und automatisierte Failover-Szenarien testen.",
                "Multi-Region-Backups und Geo-Redundanz in der Cloud nutzen, um hohe Verfügbarkeit sicherzustellen.",
                "Automatisierte Recovery-Prozesse in Cloud-Umgebungen implementieren, um Systemausfälle auf ein Minimum zu reduzieren.",
                "Datenbank-Replikation und Point-in-Time Recovery (PITR) aktiv nutzen, um verlorene Daten exakt wiederherstellen zu können."],
                {"Backup-Tools": ["Veeam", "Commvault"],
                        "AWS-Tools": ["AWS Backup", "AWS Elastic Disaster Recovery"]}
            )

        # DATENSENSIBILITÄT
        if data_sensitivity == "Personenbezogene/Firmenkritische Daten":
            display_test_method(
                "Sicherheitstests",
                "Sicherheitstests sind essenziell für den Schutz sensibler Daten vor unbefugtem Zugriff, Manipulation oder Datenlecks. "
                "Besonders personenbezogene und firmenkritische Daten müssen vor externen Angriffen sowie internen Sicherheitsrisiken geschützt werden. "
                "Diese Tests helfen, Schwachstellen frühzeitig zu erkennen und Sicherheitsmaßnahmen effektiv zu implementieren.",
                ["Sicherheitstests sind essenziell für den Schutz sensibler Daten vor unbefugtem Zugriff, Manipulation oder Datenlecks. "
                "Besonders personenbezogene und firmenkritische Daten müssen vor externen Angriffen sowie internen Sicherheitsrisiken geschützt werden. "
                "Diese Tests helfen, Schwachstellen frühzeitig zu erkennen und Sicherheitsmaßnahmen effektiv zu implementieren.",],
                ["Regelmäßige Penetrationstests durchführen, um Sicherheitslücken frühzeitig zu identifizieren.",
                "Security-Scans in den CI/CD-Prozess einbinden, um Sicherheitsprobleme direkt in der Entwicklung zu erkennen.",
                "Strenge Zugriffskontrollen nach dem Least-Privilege-Prinzip umsetzen.",
                "Ende-zu-Ende-Verschlüsselung für gespeicherte und übertragene Daten nutzen.",
                "Monitoring und Logging von sicherheitskritischen Ereignissen aktiv betreiben."],
                {"Security-Tools": ["OWASP ZAP", "Burp Suite", "AWS Security Hub"]}
            )

        # REGULATORISCHE VORGABEN
        if regulatory_requirements == "Ja":
            display_test_method(
                "Compliance-Sicherheitstests",
                "Compliance-Sicherheitstests überprüfen, ob Systeme und Prozesse gesetzliche und "
                "branchenspezifische Vorgaben einhalten. Dies ist besonders relevant für Datenschutzrichtlinien wie die "
                "DSGVO oder ISO 27001, die strenge Anforderungen an Datenverarbeitung, Sicherheit und Dokumentation stellen.",
                [ "Nicht-Einhaltung von Datenschutzrichtlinien, die zu rechtlichen Konsequenzen und hohen Strafen führen können.",
                "Fehlende Dokumentation von Sicherheits- und Datenschutzmaßnahmen, was eine Nachverfolgbarkeit und Auditierbarkeit erschwert.",
                "Unzureichende Zugriffskontrollen oder Verschlüsselungsmaßnahmen für schützenswerte Daten.",
                "Unklare Verantwortlichkeiten in der Organisation, was zu Sicherheitslücken führen kann."],
                [ "Nicht-Einhaltung von Datenschutzrichtlinien, die zu rechtlichen Konsequenzen und hohen Strafen führen können.",
                "Fehlende Dokumentation von Sicherheits- und Datenschutzmaßnahmen, was eine Nachverfolgbarkeit und Auditierbarkeit erschwert.",
                "Unzureichende Zugriffskontrollen oder Verschlüsselungsmaßnahmen für schützenswerte Daten.",
                "Unklare Verantwortlichkeiten in der Organisation, was zu Sicherheitslücken führen kann."],
                {"Compliance-Tools": ["OneTrust", "AWS Artifact"]}
            )

        # VERFÜGBARKEIT
        if availability == "Ja" and environment == "Cloud":
            display_test_method(
                "Cloud Performance-Tests",
                "Cloud Performance-Tests bewerten, ob eine Anwendung in einer Cloud-Umgebung unter variabler Last effizient skaliert "
                "und performant bleibt. Sie sind essenziell, um Engpässe zu identifizieren, die Stabilität bei Lastspitzen zu sichern "
                "und die Effizienz von Auto-Scaling-Mechanismen zu überprüfen.",
                ["Lange Antwortzeiten unter Last, insbesondere bei plötzlichen oder hohen Lastspitzen.",
                "Unzureichende Skalierungsmechanismen, die nicht schnell genug zusätzliche Ressourcen bereitstellen.",
                "Kostenexplosion durch ineffiziente Skalierungsregeln oder fehlerhafte Ressourcen-Zuweisung.",
                "Datenbank- oder Netzwerkengpässe, die zu unerwarteten Performance-Problemen führen.",
                "Mangelnde Observability, sodass Performance-Engpässe schwer zu identifizieren sind."],
                ["Lasttests mit realistischen Szenarien und Workloads durchführen, um Engpässe frühzeitig zu identifizieren.",
                "Auto-Scaling-Mechanismen aktiv nutzen und regelmäßig testen, um sicherzustellen, dass sie korrekt greifen.",
                "Monitoring und Observability mit Cloud-nativen Tools implementieren, um Performance-Flaschenhälse schnell zu erkennen.",
                "Performance-Optimierung durch Caching-Strategien, asynchrone Verarbeitung und effiziente Datenbankabfragen umsetzen.",
                "Kosten- und Kapazitätsmanagement für Cloud-Ressourcen kontinuierlich optimieren."],
                {"Cloud Performance-Tools": ["K6", "AWS CloudWatch"]}
            )

        if availability == "Ja" and environment == "On-Premise":
            display_test_method(
                "Performance-Tests",
                "Performance-Tests für On-Premise-Umgebungen bewerten die Systemleistung, Skalierbarkeit und Stabilität unter verschiedenen Lastbedingungen. "
                "Da On-Premise-Systeme oft feste Hardware-Ressourcen nutzen, sind gezielte Optimierungsmaßnahmen notwendig, um Engpässe frühzeitig zu identifizieren.",
                ["Langsame Antwortzeiten bei hoher Last aufgrund begrenzter Hardware-Ressourcen.",
                "Eingeschränkte Skalierbarkeit, da zusätzliche Hardware-Investitionen notwendig sind.",
                "Netzwerkengpässe oder hohe Latenzen durch unzureichende Bandbreite oder veraltete Infrastruktur.",
                "Unzureichende Überwachung, wodurch Performance-Probleme erst spät erkannt werden.",
                "Fehlende Kapazitätsplanung, die zu Überlastung oder ineffizienter Ressourcennutzung führt."],
                ["Regelmäßige Lasttests durchführen, um Engpässe frühzeitig zu identifizieren und Optimierungspotenziale aufzudecken.",
                "Netzwerk- und Infrastruktur-Überwachung einrichten, um Engpässe in Echtzeit zu erkennen.",
                "Kapazitätsplanung durch historische Performance-Daten optimieren, um Wachstum frühzeitig zu berücksichtigen.",
                "Caching und Load-Balancing-Techniken nutzen, um die Effizienz der Infrastruktur zu maximieren.",
                "Proaktive Wartung und regelmäßige Performance-Analysen durchführen, um Systemausfälle zu vermeiden."],
                {"Performance-Tools": ["JMeter", "Grafana"]}
            )

        # API-ABHÄNGIGKEIT
        if high_api_dependence == "Ja":
            display_test_method(
                "API-Tests",
                "API-Tests stellen sicher, dass API-Schnittstellen stabil, zuverlässig und performant sind. "
                "Da moderne Systeme stark auf APIs angewiesen sind, müssen Änderungen sorgfältig getestet werden, um Integrationsprobleme zu vermeiden.",
                ["API-Änderungen brechen bestehende Integrationen, wenn Abwärtskompatibilität nicht gewährleistet ist.",
                "Unklare oder fehlende API-Spezifikationen, die zu Missverständnissen und Implementierungsfehlern führen.",
                "Inkonsistente Antwortzeiten oder Performance-Schwankungen unter Last.",
                "Fehlende Sicherheitsmaßnahmen, wie unzureichende Authentifizierung oder unverschlüsselte Kommunikation.",
                "Unzureichende Fehlerbehandlung, die zu unerwarteten Systemverhalten oder Abstürzen führen kann."],
                ["API-Tests in die CI/CD-Pipeline integrieren, um Probleme frühzeitig zu erkennen.",
                "Mocking für API-Tests nutzen, um externe Abhängigkeiten zu minimieren und isolierte Tests zu ermöglichen.",
                "Contract-Testing einsetzen, um sicherzustellen, dass APIs erwartungsgemäße Antworten liefern.",
                "Last- und Performance-Tests für APIs durchführen, um Stabilität bei hohem Traffic zu gewährleisten.",
                "Security-Tests für API-Endpunkte implementieren, um Schwachstellen wie Injection-Angriffe oder unsichere Authentifizierung zu vermeiden."],
                {"API-Testing": ["SoapUI", "Postman", "Rest-Assured"]}
            )

        # DEPLOYMENT-FREQUENZ
        if deployment_frequency in ["Täglich", "Wöchentlich"]:
            display_test_method(
                "Statische Code-Analyse",
                "Die statische Code-Analyse überprüft den Quellcode automatisiert auf Fehler, Sicherheitslücken und Code-Smells, "
                "ohne dass der Code ausgeführt werden muss. Sie ist besonders bei häufigen Deployments essenziell, um die Codequalität "
                "kontinuierlich sicherzustellen und technische Schulden zu minimieren.",
                ["Fehler oder Sicherheitslücken werden erst spät erkannt, wenn der Code bereits produktiv ist.",
                "Unnötige technische Schulden entstehen durch nicht standardkonforme oder ineffiziente Implementierungen.",
                "Inkonsistente Code-Qualität innerhalb des Teams führt zu schlechter Wartbarkeit.",
                "Fehlende Sicherheitsprüfungen im Code können zu potenziellen Schwachstellen führen.",
                "Verstoß gegen Coding-Guidelines oder Best Practices, was langfristig die Software-Qualität beeinträchtigt."],
                ["Statische Code-Analysen in den Build-Prozess integrieren, um frühzeitige Erkennung von Fehlern zu ermöglichen.",
                "Regelmäßige Code-Reviews durchführen, um manuelle Kontrolle mit automatisierten Checks zu kombinieren.",
                "Security-Scans für Code in CI/CD-Pipelines einbinden, um Schwachstellen direkt zu identifizieren.",
                "Automatische Durchsetzung von Coding-Guidelines nutzen, um einheitlichen Code-Stil sicherzustellen.",
                "Ergebnisse aus der Code-Analyse in regelmäßigen Entwickler-Meetings besprechen, um kontinuierliche Verbesserungen zu fördern."],
                {"Code-Analyse-Tools": ["SonarQube", "Checkmarx"]}
            )

        display_test_method(
            "User Acceptance Tests (UAT)",
            "User Acceptance Tests (UAT) stellen sicher, dass das System die funktionalen und nicht-funktionalen Anforderungen der Endnutzer erfüllt. "
            "Sie sind entscheidend, um sicherzustellen, dass das System praxistauglich ist und vor der produktiven Einführung validiert wird.",
            ["Das System erfüllt die Anforderungen der Nutzer nicht, weil geschäftskritische Prozesse nicht realitätsnah getestet wurden.",
            "Unverständliche oder nicht intuitive Bedienung führt zu einer schlechten Benutzerakzeptanz.",
            "Fehlende oder unklare Abnahmekriterien erschweren eine objektive Bewertung der Testergebnisse.",
            "Unzureichende Testabdeckung, da nicht alle relevanten Nutzungsszenarien berücksichtigt wurden.",
            "Kommunikationsprobleme zwischen Entwicklern und Fachanwendern führen zu Missverständnissen."],
            ["Echte Endnutzer in den Testprozess einbinden, um praxisnahe Szenarien zu validieren.",
            "Klar definierte Abnahmekriterien und Testfälle formulieren, um objektive Ergebnisse sicherzustellen.",
            "Frühzeitige Prototypen oder Beta-Versionen bereitstellen, um frühzeitig Feedback aus der Praxis zu erhalten.",
            "Exploratives Testen zulassen, um unvorhergesehene Probleme aufzudecken.",
            "Testdokumentation nutzen, um Nachvollziehbarkeit und Vergleichbarkeit der Ergebnisse zu gewährleisten."],
            {"Dokumentation": ["Jira", "Confluence"]}
        )

        display_test_method(
            "End-to-End-Tests",
            "End-to-End-Tests (E2E-Tests) stellen sicher, dass das gesamte System, von Frontend über Backend bis zur Datenbank, "
            "in einer realistischen Umgebung einwandfrei funktioniert. Diese Tests sind essenziell, um sicherzustellen, dass alle "
            "Systemkomponenten korrekt miteinander interagieren und komplexe Benutzerworkflows stabil ablaufen.",
            ["Unstimmigkeiten zwischen Backend und Frontend führen zu unerwartetem Verhalten oder fehlerhaften Datenanzeigen.",
            "Fehler durch Dateninkonsistenzen zwischen verschiedenen Systemkomponenten, die nicht synchronisiert sind.",
            "Nicht getestete Schnittstellen verursachen Integrationsprobleme bei der Kommunikation zwischen Services.",
            "Skalierungsprobleme, die in isolierten Tests nicht sichtbar werden, treten in realen Nutzungsszenarien auf.",
            "Testfälle sind schwer wartbar oder instabil, wenn sie nicht sinnvoll automatisiert werden."],
            ["Tests unter produktionsnahen Bedingungen durchführen, um realistische Szenarien abzubilden.",
            "Komplexe Benutzerworkflows testen, um sicherzustellen, dass alle Schritte korrekt funktionieren.",
            "Automatisierung gezielt einsetzen, insbesondere für wiederholbare Testfälle mit hohem Mehrwert.",
            "Datenbank- und API-Tests in die End-to-End-Tests integrieren, um Datenfluss und Konsistenz sicherzustellen.",
            "Parallele Testausführung nutzen, um die Laufzeit von umfangreichen E2E-Tests zu reduzieren."],
            {"Testautomatisierung": ["Selenium", "Playwright", "Cypress"]}
        )

output =output = BytesIO()
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    workbook = writer.book
    worksheet = workbook.add_worksheet("Testmethoden")
    writer.sheets["Testmethoden"] = worksheet

    # Formatierung für besseren Export
    wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})  # Mehrzeilig & oben ausgerichtet
    bold_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top'})  # Mehrzeilig mit Fettschrift

    # System-/Service-Name & Beschreibung platzieren
    worksheet.write(0, 0, "System-/Service-Name:", bold_format)
    worksheet.write(0, 1, system_name, wrap_format)
    worksheet.write(1, 0, "Beschreibung:", bold_format)
    worksheet.write(1, 1, system_description, wrap_format)

    # Testmethoden-Übersicht (Falls keine Empfehlungen existieren, wird das verhindert)
    if test_recommendations:
        test_data = {"": ["Beschreibung", "Häufige Probleme", "Best Practices", "Eingesetzte Tools"]}

        for rec in test_recommendations:
            test_name = rec.get("Testmethode", "Unbenannte Methode")
            test_data[test_name] = [
                rec.get("Beschreibung", ""),
                "\n".join(rec.get("Häufige Probleme", "").split(". ")),  # Automatischer Umbruch nach Punkten
                "\n".join(rec.get("Best Practices", "").split(". ")),
                rec.get("Eingesetzte Tools", "")
            ]

        df_tests = pd.DataFrame.from_dict(test_data, orient="index").transpose()

        # Testmethoden ab Zeile 4 einfügen
        df_tests.to_excel(writer, sheet_name="Testmethoden", index=False, startrow=3, startcol=0)

        # **Spaltenbreite begrenzen (max 50 Zeichen)**
        for i, col in enumerate(df_tests.columns):
            worksheet.set_column(i, i, 50, wrap_format)  # Max. 50 Zeichen Breite

        # **Zeilenhöhe für bessere Lesbarkeit**
        worksheet.set_row(4, 50, wrap_format)  # Zeilenhöhe für "Beschreibung" erhöhen
        for row_num in range(5, len(df_tests) + 5):
            worksheet.set_row(row_num, 30, wrap_format)  # Restliche Zeilen auch anpassen

output.seek(0)

# Download-Button für die Excel-Datei
if test_recommendations:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"Testmethoden_Empfehlung_{timestamp}.xlsx"

    st.download_button(
        label="Als Excel herunterladen",
        data=output,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
