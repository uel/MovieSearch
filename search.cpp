#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <filesystem>
#include "helper_functions.h"
#include <math.h>
#include <queue>
using namespace std;

unordered_map<string, pair<int, int>> LoadIndex(string filename)
{
    unordered_map<string, pair<int, int>> map;
    ifstream file(filename);
    string line;
    while (getline(file, line))
    {
        string key;
        int value1, value2;
        stringstream ss(line);
        ss >> key >> value1 >> value2;
        map[key] = make_pair(value1, value2);
    }
    file.close();
    return map;
}

const unordered_map<string, pair<int, int>> index(LoadIndex("data/index.txt"));
vector<Node> inverted_index;
ifstream inverted_index_file("data/inverted_index.bin", ios::binary);
bool load_inverted_index = false;

Node InvertedIndex(size_t i)
{
    if (load_inverted_index)
        return inverted_index[i];
    else
    {
        inverted_index_file.seekg(i * sizeof(Node));
        Node node;
        inverted_index_file.read((char *)&node, sizeof(Node));
        return node;
    }
}

float cosine_similarity(vector<float>& v1, vector<float>& v2)
{
    float p = 0, m1 = 0, m2 = 0;

    for (int i = 0; i < v1.size(); i++)
    {
        p += v1[i] * v2[i];
        m1 += pow(v1[i], 2);
        m2 += pow(v2[i], 2);
    }

    m1 = sqrt(m1);
    m2 = sqrt(m2);

    float result = 0;
    if (m1 != 0 && m2 != 0)
        result = p / (m1 * m2);

    return result;
}

vector<int> Search(unordered_map<string, float> query, int k = 50)
{
    vector<size_t> initial, sizes, offsets(query.size(), 0);
    vector<string> terms; vector<float> query_vector;
    for (auto i : query)
    {
        terms.push_back(i.first);
        query_vector.push_back(i.second);
        initial.push_back(index.at(i.first).first/8);
        sizes.push_back(index.at(i.first).second);
    }

    priority_queue<pair<float, int>, vector<pair<float, int>>> result;

    while (true)
    { 
        int min = 10000000;
        vector<float> doc_vector(query.size(), 0);
        for (int i = 0; i < query.size(); i++)
        {
            if (offsets[i] < sizes[i])
            {
                if ( InvertedIndex(initial[i] + offsets[i]).doc_id < min )
                {
                    min = InvertedIndex(initial[i] + offsets[i]).doc_id;
                    fill(doc_vector.begin(), doc_vector.end(), 0);
                }
                if ( InvertedIndex(initial[i] + offsets[i]).doc_id == min )
                    doc_vector[i] = InvertedIndex(initial[i] + offsets[i]).weight;
            }
        }

        if ( min == 10000000 ) break;

        for (size_t i = 0; i < query.size(); i++)
            if (doc_vector[i] != 0) {
                offsets[i]++;    
            }

        float distance = cosine_similarity(query_vector, doc_vector);
        result.push(make_pair(distance, min));
    }

    vector<int> result_vector;
    for (size_t i = 0; i < k; i++)
    {
        result_vector.push_back(result.top().second);
        result.pop();
    }
    
    return result_vector;
}

int main(int argc, char const *argv[])
{
    load_inverted_index = true;
    size_t size = 1149116264; //std::ifstream("data/inverted_index.bin", std::ifstream::ate | std::ifstream::binary).tellg(); 
    if ( load_inverted_index )
    {
        inverted_index.resize(size/sizeof(Node));
        inverted_index_file.read((char*)&inverted_index[0], size);
    }

    while (true)
    {
        string line;
        getline(cin, line);
        if (line == "") break;
        stringstream ss(line);
        string term;
        float weight;
        unordered_map<string, float> query;
        while (ss >> term >> weight) query[term] = weight;

        auto res = Search(query);

        for (auto i : res)
            cout << i << " ";
        cout << endl;
    }

    inverted_index_file.close();
    return 0;
}
