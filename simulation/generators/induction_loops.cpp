#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <string>

std::string value_between(std::string &source, std::string a, std::string b) {
	size_t found1 = source.find(a);
	size_t found2 = source.find(b, found1 + a.length());

	std::string value(source.begin() + found1 + a.length(), source.begin() + found2);
	return value;
}

int main() {
	std::ifstream file_in("simulation.net.xml");
	std::ofstream file_out("my.det.xml");
	std::string line;
	char out_line[256];
	bool is_edge = false;

	file_out << "<additional>\n";

	while (getline(file_in, line)) {
		if (is_edge) {
			std::string id = value_between(line, "id=\"", "\"");
			double length = atof(value_between(line, "length=\"", "\"").c_str());
			static double place = length * 0.05;

			sprintf(out_line, "\t<inductionLoop id=\"%s\" lane=\"%s\" pos=\"%.2lf\" freq=\"30\" file=\"out.xml\"/>\n", (id + 'a').c_str(), id.c_str(), place);
			file_out << out_line;
			sprintf(out_line, "\t<inductionLoop id=\"%s\" lane=\"%s\" pos=\"%.2lf\" freq=\"30\" file=\"out.xml\"/>\n", (id + 'b').c_str(), id.c_str(), -place);
			file_out << out_line;

			is_edge = false;
			continue;
		}

		if (line.find("<edge id") != std::string::npos && line.find("internal") == std::string::npos)
			is_edge = true;
	}

	file_out << "</additional>\n";

	file_in.close();
	file_out.close();
	return 0;
}
