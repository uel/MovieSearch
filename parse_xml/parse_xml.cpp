#include <boost/algorithm/string.hpp>
#include <iostream>
#include <fstream>
#include <experimental/filesystem>
#include "pugixml.hpp"
#include <boost/algorithm/string/trim.hpp>
#include <unordered_set>

using namespace std;

int main()
{
    unordered_set<string> created;

    int n = 0;

    for (auto f : experimental::filesystem::recursive_directory_iterator("../data/extracted"))
    {
        string source = f.path();
        if (!source.ends_with(".xml")) continue;

        std::cout << f << endl;

        string movieId = source;
        boost::replace_first(movieId, "../data/raw/en/", "");
        movieId = movieId.substr(movieId.find("/")+1);
        string subId = movieId.substr(movieId.find("/")+1, movieId.length() - movieId.find("/") - 5);
        movieId = movieId.substr(0, movieId.find("/"));

        if ( created.count(movieId) ) continue;
        created.insert(movieId);

        string target = "../data/parsed/"+subId+".txt";

        n++;
        if ( n % 100 ) cout << "n " << n << " : " << movieId << " " << subId << source << endl;

        ofstream out;
        out.open(target, ios::out | ios::trunc );
        pugi::xml_document doc;
        pugi::xml_parse_result result = doc.load_file(source.c_str());
        for (pugi::xml_node l : doc.child("document").children("s"))
        {
            string s(l.child_value());
            boost::algorithm::trim(s);
            out << s << endl;
        }
        out.close();
    }
}