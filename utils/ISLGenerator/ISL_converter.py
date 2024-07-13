# Imports
import re , os , nltk
import nltk.parse.stanford
from nltk import ParentedTree, Tree
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Globals
JAVA_PATH = r"C:\Program Files\Java\jre-1.8\bin\javaw.exe"
STANF_PARSER_PATH = r"stanford-parser-full-2018-02-27\stanford-parser.jar"
STANF_MODELS_PATH = r"stanford-parser-full-2018-02-27\stanford-parser-3.9.1-models.jar"

# NLTK Downloads
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

# Environment Set
os.environ['JAVAHOME'] = JAVA_PATH

# Parser Directions
sp = nltk.parse.stanford.StanfordParser(path_to_jar = STANF_PARSER_PATH , path_to_models_jar = STANF_MODELS_PATH)

# Converter Class
class ISLConverter:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords_set = set(stopwords.words('english'))

    def convert_isl(self, parsetree):
        dict = {}
        parenttree = ParentedTree.convert(parsetree)
        for sub in parenttree.subtrees():
            dict[sub.treeposition()] = 0

        self.isltree = Tree('ROOT', [])
        i = 0

        for sub in parenttree.subtrees():
            if sub.label() == "NP" and dict[sub.treeposition()] == 0 and dict[sub.parent().treeposition()] == 0:
                dict[sub.treeposition()] = 1
                self.isltree.insert(i, sub)
                i += 1
            if sub.label() == "VP" or sub.label() == "PRP":
                for sub2 in sub.subtrees():
                    if (sub2.label() == "NP" or sub2.label() == 'PRP') and dict[sub2.treeposition()] == 0 and dict[
                        sub2.parent().treeposition()] == 0:
                        dict[sub2.treeposition()] = 1
                        self.isltree.insert(i, sub2)
                        i += 1

        for sub in parenttree.subtrees():
            for sub2 in sub.subtrees():
                if len(sub2.leaves()) == 1 and dict[sub2.treeposition()] == 0 and dict[
                    sub2.parent().treeposition()] == 0:
                    dict[sub2.treeposition()] = 1
                    self.isltree.insert(i, sub2)
                    i += 1

        return self.isltree

    def text_to_isl(self, sentence):
        pattern = r'[^\w\s]'
        sentence = re.sub(pattern, '', sentence)
        englishtree = [tree for tree in sp.parse(sentence.split())]
        parsetree = englishtree[0]
        self.isl_tree = self.convert_isl(parsetree)
        words = parsetree.leaves()
        lemmatized_words = [self.lemmatizer.lemmatize(w) for w in words]
        islsentence = " ".join([w for w in lemmatized_words if w not in self.stopwords_set])
        islsentence = islsentence.lower()
        self.isltree = [tree for tree in sp.parse(islsentence.split())]
        return islsentence

