#ifndef SEED_H_
#define SEED_H_

#include <stdlib.h>
#include <vector>
#include <string>
#include <iostream> 
#include <stdint.h>
#include "pattern.h"


#define MAX_BUCKETS 256

class Seed{
	private:
		int32_t length;
		int32_t weight;
		int32_t dontCare;
		std::vector<char> dontCarePos;
		std::vector<char> matchPos;

	public:

		Seed(int32_t, int32_t );
		void generatePattern();

		int32_t getLength();
		int32_t getWeight();
		int32_t getDontCare();

		void fillDontCare(std::vector<char> &, char *);
		void fillDontCareScore(std::vector<char> & vec, char * seq);
		char getMismatches(std::vector<char> & ,std::vector<char> &);
		int32_t getScore(std::vector<char> & ,std::vector<char> &);

		void getFirstWord(unsigned char &, char *);
		void getNextWord(uint32_t &, char *);

		static void init();
		static unsigned char alphabet[MAX_BUCKETS];
		static unsigned char alphabetRev[MAX_BUCKETS];
		static char score[4][4];
};

#endif