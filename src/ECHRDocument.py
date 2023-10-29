import os
import re
import json
from bs4 import BeautifulSoup
import PyPDF2


class ECHRDocument:
    """
    Classe che rappresenta una pronuncia della Corte Europea dei Diritti dell'Uomo
    """

    # TODO: se possibile sostituire file html con url, ma non è semplice perché il sito non è statico.
    #  Il contenuto dei file è copiato da "Inspect" di Chrome
    def __init__(self, html_path: str = None, pdf_path: str = None, file_name: str = None):
        """
        :param html_path: percorso in cui si trova il file html che contiene il documento
        :param pdf_path: percorso in cui si trova il file pdf che contiene il documento
        :param file_name: nome del file SENZA ESTENSIONE
        """
        if html_path is not None and file_name is not None:
            path = html_path + "/" + file_name + ".html"
            if not os.path.exists(path):
                raise Exception(f"PATH ERROR (HTML): {os.path.abspath(path)} does not exist")
        if pdf_path is not None and file_name is not None:
            path = pdf_path + "/" + file_name + ".pdf"
            if not os.path.exists(path):
                raise Exception(f"PATH ERROR (PDF): {os.path.abspath(path)} does not exist")
        self._html_path = html_path
        self._pdf_path = pdf_path
        self._file_name = file_name
        self._case_detail = None
        self._body = None
        self._footnotes = None
        self._triples = []
        self._titles = []

    def __str__(self):
        if self._file_name is None:
            return "Not initialized"
        return self._file_name

    def set_html_path(self, html_path: str) -> None:
        if html_path is not None and self._file_name is not None:
            path = html_path + "/" + self._file_name + ".html"
            if not os.path.exists(path):
                raise Exception(f"PATH ERROR (HTML): {os.path.abspath(path)} does not exist")
        self._html_path = html_path

    def get_html_path(self) -> str:
        return self._html_path

    def set_pdf_path(self, pdf_path: str) -> None:
        if pdf_path is not None and self._file_name is not None:
            path = pdf_path + "/" + self._file_name + ".pdf"
            if not os.path.exists(path):
                raise Exception(f"PATH ERROR (PDF): {os.path.abspath(path)} does not exist")
        self._pdf_path = pdf_path

    def get_pdf_path(self) -> str:
        return self._pdf_path

    def set_file_name(self, file_name: str) -> None:
        if (self._pdf_path is not None or self._html_path is not None) and self._file_name is not None:
            if self._pdf_path is not None:
                path = self._pdf_path + "/" + file_name + ".pdf"
            else:
                path = self._html_path + "/" + file_name + ".html"
            if not os.path.exists(path):
                raise Exception(f"PATH ERROR: {os.path.abspath(path)} does not exist")
        self._file_name = file_name

    def get_file_name(self) -> str:
        return self._file_name

    def extract_case_detail_from_html(self):
        """
        Estrae il contenuto della tab "Case Details" di un caso dal sito hudoc.echr.coe.int
        Ad esempio da https://hudoc.echr.coe.int/eng#{%22itemid%22:[%22001-58371%22]} si ottiene il seguente dizionario:
            Originating Body: Court (Grand Chamber)
            Document Type: Judgment (Merits and Just Satisfaction)
            Published in: Reports 1997-VI
            Title: CASE OF AYDIN v. TURKEY
            App. No(s).: 23178/94
            Importance Level: 1
            Represented by: N/A
            Respondent State(s): Türkiye
            Reference Date: 15/04/1996
            Judgment Date: 25/09/1997
            Conclusion(s): ['Preliminary objection rejected (estoppel)', 'Violation of Art. 3', 'Violation of Art. 13', 'Not necessary to examine Art. 6-1', 'No violation of Art. 25-1', 'Not necessary to examine Art. 28-1-a', 'Not necessary to examine Art. 53', 'Pecuniary damage - claim dismissed', 'Non-pecuniary damage - financial award', 'Costs and expenses partial award - Convention proceedings']
            Article(s): ['3', '6', '6-1', '13', '25', '25-1', '28', '28-1-a', '46', '46-1', '41', '34', '53']
            Separate Opinion(s): Yes
            Domestic Law: ['Criminal Code, Articles 179, 181, 191, 243, 245 and 416 ', 'Code of Criminal Procedure, Articles 153, 154, 163 and 165 ', 'Constitution, Article 125 ', 'Military Criminal Code, Article 152 ', 'Civil Code, Articles 41, 46 and 47 ', 'Decree no. 285 modifying the application of Law no. 3713, the Anti-Terror Law (1981) ', 'Law no. 2935 of 25 October 1983 on the state of emergency, section 1']
            Strasbourg Case-Law: ['Ireland v. the United Kingdom judgment of 18 January 1978, Series A no. 25, pp. 64-65, §§ 160-161, p. 66, § 167', 'The Holy Monasteries v. Greece judgment of 9 December 1994, Series A no. 301-A, pp. 36-37, § 80', 'Loizidou v. Turkey judgment of 23 March 1995 (preliminary objections), Series A no. 310, p. 19, § 44', 'Akdivar and Others v. Turkey judgment of 16 September 1996, Reports of Judgments and Decisions ("Reports") 1996-IV, p. 1219, § 105', 'Aksoy v. Turkey judgment of 18 December 1996, Reports 1996-VI, p. 2272, § 38, p. 2278, § 62, p. 2285, § 92, p. 2286, § 95, p. 2287, § 98']
            International Law: United Nations Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment of 10 December 1984, Articles 11, 12 and 13
            Keywords: ['(Art. 3) Prohibition of torture', '(Art. 3) Torture', '(Art. 13) Right to an effective remedy', '(Art. 13) Effective remedy', '(Art. 34) Individual applications', '(Art. 34) Individual', '(Art. 34) Hinder the exercise of the right of application', '(Art. 6) Right to a fair trial', '(Art. 46) Binding force and execution of judgments', '(Art. 41) Just satisfaction-{general}', '(Art. 53) Rights otherwise guaranteed']
            ECLI: ECLI:CE:ECHR:1997:0925JUD002317894

            I valori possono essere stringhe o liste di stringhe a seconda dei casi
        :return:
        """

        if self._html_path is None or self._file_name is None:
            return
        try:
            html = open(self._html_path + "/" + self._file_name + ".html", "r", encoding="UTF-8").read()
        except Exception as e:
            print(f"\033[1;31m{e}\033[0m")
            return
        soup = BeautifulSoup(html, 'html.parser')
        """
        div id="notice" contenente sezione dei case detail
        div class="row noticefield" contenente la riga
        div class="span2 noticefieldheading" contenente il nome del campo
        div class="col-offset-2 noticefieldvalue" contiene il valore del campo
        """
        heading_list = soup.find_all("div", {"class": "span2 noticefieldheading"})
        value_list = soup.find_all("div", {"class": "col-offset-2 noticefieldvalue"})

        case_detail = {}
        for i in range(len(heading_list)):
            key = heading_list[i].text
            values = re.split(r'\t+\s*', value_list[i].text.strip().replace("more…", ""))
            if len(values) == 1:
                case_detail[key] = values[0]
            else:
                case_detail[key] = values
        self._case_detail = case_detail

    def get_case_detail(self) -> dict:
        return self._case_detail

    def case_detail_to_json(self, path: str):
        """
        :param path: percorso in cui salvare il file json
        :return:
        """
        if self._case_detail is None:
            return
        name = self._file_name + ".json"
        try:
            with open(path + "/" + name, "w", encoding="UTF-8") as f:
                json.dump(self._case_detail, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\033[1;31m{e}\033[0m")

    def extract_body_from_html(self):
        """
        estrae il corpo del documento e le eventuali note a piè di pagina di una pagina dal sito hudoc.echr.coe.int
        :return:
        """
        if self._html_path is None or self._file_name is None:
            return
        try:
            html = open(self._html_path + "/" + self._file_name + ".html", "r", encoding="UTF-8").read()
        except Exception as e:
            print(f"\033[1;31m{e}\033[0m")
            return
        soup = BeautifulSoup(html, 'html.parser')
        """
        div id="document" contiene il testo del documento
        div id="_ftn[i]" contiene la nota a piè di pagina
        """
        document_text = soup.find("div", {"id": "document"}).text
        footnote_list = soup.find_all("div", {"id": re.compile(r"_ftn\d+")})
        footnote_text = ""
        if len(footnote_list) != 0:
            for footnote in footnote_list:
                document_text = document_text.replace(footnote.text, "")
                footnote_text += footnote.text + "\n"
            self._footnotes = footnote_text
        self._body = document_text

    def get_body(self) -> str:
        return self._body

    def get_footnotes(self) -> str:
        return self._footnotes

    def body_to_txt(self, path: str):
        """
        :param path: percorso in cui salvare il file txt
        :param path:
        :return:
        """
        if self._body is None:
            return
        try:
            with open(path + "/" + self._file_name + ".txt", "w", encoding="UTF-8") as f:
                f.write(self._body)
        except Exception as e:
            print(f"\033[1;31m{e}\033[0m")

    def footnotes_to_txt(self, path: str):
        """
        :param path: percorso in cui salvare il file txt
        :param path:
        :return:
        """
        if self._footnotes is None:
            return
        try:
            with open(path + "/" + self._file_name + ".txt", "w", encoding="UTF-8") as f:
                f.write(self._footnotes)
        except Exception as e:
            print(f"\033[1;31m{e}\033[0m")

    def extract_titles(self):
        # TODO se torna utile, migliorare implementazione
        if self._pdf_path is None or self._file_name is None:
            return
        path = self._pdf_path + "/" + self._file_name + ".pdf"
        try:
            titles = []
            pdf_file = open(path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                # i titoli delle sezioni principali sono in maiuscolo
                for sentence in text.split('\n'):
                    if sentence.isupper():
                        titles.append(sentence)
            self._titles = titles
        except Exception as e:
            print(f"\033[1;31m{e}\033[0m")

    def get_titles(self) -> list:
        return self._titles

    def extract_triples_from_case_detail(self):
        # TODO implementato in modo molto naive => MODIFICARE
        if self._case_detail is None:
            return
        SUBJECT = 'App. No(s).'
        CASE_DETAIL_ECLI_MAP = {
            'Originating Body': 'dcterms:creator',
            'Document Type': 'dcterms:type',
            'Title': 'dcterms:title',
            'Represented by': 'dcterms:contributor',
            'Judgment Date': 'dcterms:date',
            'Decision Date': 'dcterms:date',
            'Conclusion(s)': 'dcterms:abstract',
            'Domestic Law': 'dcterms:references',
            'Strasbourg Case-Law': 'dcterms:references',
            'International Law': 'dcterms:references',
            'Keywords': 'dcterms:description',
            'ECLI': 'dcterms:isVersionOf',
        }
        # EX = "http://example.org/#"
        EX = "ex:"
        s = EX + self._case_detail[SUBJECT]
        matching_keys = set(self._case_detail.keys()).intersection(set(CASE_DETAIL_ECLI_MAP.keys()))
        for key in matching_keys:
            p = CASE_DETAIL_ECLI_MAP[key]
            if type(self._case_detail[key]) == str:
                o = EX + self._case_detail[key].replace(" ", "_").replace("(", "").replace(")", "")
                self._triples.append({"subject": s, "predicate": p, "object": o})
            else:
                for value in self._case_detail[key]:
                    o = EX + value.replace(" ", "_").replace("(", "").replace(")", "").replace("{", "").replace("}", "")
                    self._triples.append({"subject": s, "predicate": p, "object": o})

    def extract_triples_from_body(self):
        # TODO implementare
        if self._body is None:
            return
        pass

    def get_triples(self) -> list:
        return self._triples

    def save_triples(self):
        # TODO implementare
        pass


def test():
    """
    prova di utilizzo della classe
    :return:
    """
    if __name__ != "__main__":
        return
    import pprint
    html = "../data/corpus_html"
    pdf = "../data/corpus_pdf"
    name = "CASE OF A. v. CROATIA"
    json_path = "../data/case_detail_json"
    body_path = "../data/document_body"
    echr_document = ECHRDocument(html_path=html, pdf_path=pdf, file_name=name)
    print("DOCUMENT___________________________________________________________________________________________________")
    print(echr_document)
    echr_document.extract_case_detail_from_html()
    print("CASE DETAIL________________________________________________________________________________________________")
    pprint.pprint(echr_document.get_case_detail(), sort_dicts=False)
    echr_document.case_detail_to_json(json_path)
    echr_document.extract_body_from_html()
    print("BODY_______________________________________________________________________________________________________")
    print(echr_document.get_body())
    print("FOOTNOTES__________________________________________________________________________________________________")
    print(echr_document.get_footnotes())
    echr_document.body_to_txt(body_path)
    print("TITLES_____________________________________________________________________________________________________")
    echr_document.extract_titles()
    for t in echr_document.get_titles():
        print(t)
    print("TRIPLES____________________________________________________________________________________________________")
    echr_document.extract_triples_from_case_detail()
    for t in echr_document.get_triples():
        print(t)


test()
