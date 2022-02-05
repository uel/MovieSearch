#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <filesystem>
#include "helper_functions.h"
#include <math.h>
#include <algorithm>
using namespace std;

int main(int argc, char const *argv[])
{
    unordered_map<string, int> document_frequency = LoadMap("data/document_freq.txt");
    unordered_map<string, int> max_frequency = LoadMap("data/max_freq.txt");
    vector<string> terms = LoadLines("data/terms.txt");
    vector<string> documents = LoadLines("data/documents.txt");

    float document_count = documents.size();

    unordered_map<string, vector<Node>> inverted_index;

    unsigned int i = 0;
    for ( auto& p : filesystem::directory_iterator("data/tokenized") )
    {
        ifstream file(p.path().string());

        string term;
        float freq;
        while ( file >> term )
        {
            file >> freq;
            float weight = (freq/max_frequency[term])*log2(document_count/document_frequency[term]);
            Node node { (uint32_t)stoi(p.path().stem().string()), weight };
            inverted_index[term].push_back(node);
        }
        file.close();

        cout << "\r" << p.path().string() << " Progress: " << i++ << "/" << documents.size() << flush;
    }
    cout << endl;

    unordered_map<string, int> index;
    ofstream result("data/inverted_index.bin", ios::binary);
    i = 0;
    for ( string t : terms )
    {
        sort(inverted_index[t].begin(), inverted_index[t].end(), [](Node a, Node b){ return a.doc_id < b.doc_id; });
        index[t] = result.tellp();
        result.write((char*)&inverted_index[t][0], sizeof(Node)*inverted_index[t].size());
        cout << "\r" << "Saving: " << i++ << "/" << terms.size() << flush;
    }
    result.close();
    SaveMap("data/index.txt", index);

    return 0;
}
