import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom

def read_apologies(path, langs):
    to_return = dict()

    ap = open(os.path.join(path, "English.txt"), "r").read().split("\n")
    for s in ap:
        s = s.strip()
    to_return["English"] = ap

    ap = open(os.path.join(path, "Chinese.txt"), "r").read().split("\n")
    for s in ap:
        s = s.strip()
    to_return["Chinese"] = ap

    for lang in langs:
        lang_path = os.path.join(path, lang)
        ap = open(os.path.join(lang_path, lang+".txt"), "r").read().split("\n")
        for s in ap:
            s = s.strip()
        to_return[lang] = ap
        if lang == "Kanakanavu":
            ap = open(os.path.join(lang_path, lang+"_en.txt"), "r").read().split("\n")
            for s in ap:
                s = s.strip()
            to_return[lang+"_en"] = ap

            ap = open(os.path.join(lang_path, lang+"_zh.txt"), "r").read().split("\n")
            for s in ap:
                s = s.strip()
            to_return[lang+"_zh"] = ap
    return to_return

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # print(reparsed.toprettyxml(indent="    "))
    return reparsed.toprettyxml(indent="    ")


def generate_apology_xml(lang, lang_code, apologies, out_path):


    root = Element("TEXT")
    root.set("id", f"PA_{lang}")
    root.set("xml:lang", lang_code)
    root.set("citation", "")
    root.set("BibTeX_citation", "")
    root.set("copyright", "public domain")

    print(len(apologies[lang]), lang)
    apology, en, zh = apologies[lang], apologies["English"], apologies["Chinese"]
    if lang == "Kanakanavu":
        en, zh = apologies[lang + "_en"], apologies[lang + "_zh"]

    for i in range(len(apology)):
        ap_s, en_s, zh_s = apology[i], en[i], zh[i]
        s_element = SubElement(root, "S")
        s_element.set("id", str(i))
        
        form_element = SubElement(s_element, "FORM")
        form_element.text = ap_s

        transl_element = SubElement(s_element, "TRANSL")
        transl_element.set("xml:lang", "zh")
        transl_element.text = zh_s
       
        transl_element = SubElement(s_element, "TRANSL")
        transl_element.set("xml:lang", "en")
        transl_element.text = en_s


    try:
        xml_string = prettify(root)
    except:
        xml_string = ""
        print(lang)

    with open(os.path.join(out_path, lang+".xml"), "w", encoding="utf-8") as xmlfile:
        xmlfile.write(xml_string)

def main():
    
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(curr_dir, "Apologies_XML")

    lang_codes = {"Amis":"ami", "Atayal":"tay", "Saisiyat":"xsy", "Thao":"ssf", "Seediq":"trv", "Bunun":"bnn", 
                  "Paiwan":"pwn", "Rukai":"dru", "Truku":"trv", "Kavalan":"ckv", "Tsou":"tsu", "Kanakanavu":"xnb", 
                  "Saaroa":"sxr", "Puyuma":"pyu", "Yami":"tao", "Sakizaya":"szy"}
    
    langs = ["Amis", "Atayal", "Bunun", "Kavalan", "Paiwan", "Puyuma", "Rukai", "Saaroa", "Saisiyat", "Sakizaya", 
             "Seediq", "Thao", "Truku", "Tsou", "Yami", "Kanakanavu"]
    apologies_dir = os.path.join(curr_dir, "Apologies")
    apologies = read_apologies(apologies_dir, langs)
    for lang in langs:
        generate_apology_xml(lang, lang_codes[lang], apologies, output_path)

    
if __name__ == "__main__":
    main()
