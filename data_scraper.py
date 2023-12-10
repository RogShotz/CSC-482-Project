import wikipediaapi
from csv import writer
from nltk import sent_tokenize
from people_with_wikipedia_articles import people_with_wikipedia_articles

wiki_wiki = wikipediaapi.Wikipedia('CSC482: Geneaology Project', 'en')

familial_relationship_substrings = [
    "parent", "child", "sibling", "grand", "mo", "father", "dad", "son", "daughter", "sister", "brother"
]

def get_subsections(section):
    text_list = [section.text]
    for s in section.sections:
        text_list += get_subsections(s)
    return text_list

def main():
    with open("wikipedia_data.csv", "w", encoding="utf8") as f:
        w = writer(f, lineterminator='\n')
        for person in people_with_wikipedia_articles:
            page_py = wiki_wiki.page(person)

            sections = []
            for s in page_py.sections:
                if "life" in s.title.lower() or "family" in s.title.lower():
                    sections.append(s.text)
                    sections += get_subsections(s)
            
            for section in sections:
                for sentence in sent_tokenize(section):
                    for string in familial_relationship_substrings:
                        if string in sentence:
                            w.writerow([sentence.strip()])
                            break

                


if __name__ == "__main__":
    main()