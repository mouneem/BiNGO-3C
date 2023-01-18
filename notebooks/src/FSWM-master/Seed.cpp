#include "Seed.h"

unsigned char Seed::alphabet[] = { 0 };
unsigned char Seed::alphabetRev[] = { 0 };
char Seed::score[4][4] ={{91,-114,-31,-123},
						{-114, 100, -125, -31},
						{-31, -125, 100, -114},
						{-123, -31, -114, 91}};
/*char Seed::score[4][4] ={{0,2,1,2},
						{2, 0, 2, 1},
						{1, 2, 0, 2},
						{2, 1, 2, 0}};*/

Seed::Seed(int32_t weight, int32_t dontCare)
{
	this->weight=weight;
	this->dontCare=dontCare;
	this->length=weight+dontCare;
	generatePattern();
}

void Seed::generatePattern()
{
	pattern* pattern_obj;
	pattern_obj = new pattern(NULL, NULL, 1, weight + dontCare, weight, 10000, 10000, 10000, 0.75, 0.25);
	pattern_obj->ImproveSecure();
	pattern_obj->Improve(5000);
	std::string pattern=pattern_obj->GetBestPattern(0);
	//std::string pattern="10010000000000000010000001000000000000001000000000000000000000000000000010000000000100010000000000001000000001";
	for(int32_t i = 0; i < pattern.length(); i++)
	{
		if (pattern[i] == '1')
			matchPos.push_back(i);
		else
			dontCarePos.push_back(i);
	}
}

int32_t Seed::getLength()
{
	return length;
}

int32_t Seed::getWeight()
{
	return weight;
}

int32_t Seed::getDontCare()
{
	return dontCare;
}

void Seed::init()
{
	Seed::alphabet['A'] = 0;
	Seed::alphabet['C'] = 1;
	Seed::alphabet['G'] = 2;
	Seed::alphabet['T'] = 3;
	Seed::alphabetRev['A'] = 3;
	Seed::alphabetRev['C'] = 2;
	Seed::alphabetRev['G'] = 1;
	Seed::alphabetRev['T'] = 0;

}

char Seed::getMismatches (std::vector<char> & dontCareRef, std::vector<char> & dontCareQry)
{
	char mm=0;
	for(uint32_t i = 0; i < dontCare; i++)
	{
		if(dontCareRef[i] != dontCareQry[i])
			mm++;
	}
	return mm;
}

/*int32_t Seed::getScore (std::vector<char> & dontCareRef, std::vector<char> & dontCareQry)
{
	int32_t score=0;
	int32_t totalScore=0;
	for(uint32_t i = 0; i < 10; i++)
	{
		score += Seed::score[dontCareRef[i]][dontCareQry[i]];
	}
	if(score<0)
		return -1;
	totalScore+=score;
	score=0;
	for(uint32_t i = 10; i < 90; i++)
	{
		score += Seed::score[dontCareRef[i]][dontCareQry[i]];
	}
	if(score<0)
		return -1;
	totalScore+=score;
	score=0;
	for(uint32_t i = 90; i < 100; i++)
	{
		score += Seed::score[dontCareRef[i]][dontCareQry[i]];
	}
	if(score<0)
		return -1;
	totalScore+=score;
	return totalScore;
}*/

/*int32_t Seed::getScore (std::vector<char> & dontCareRef, std::vector<char> & dontCareQry)
{
	int32_t score1=0;
	for(uint32_t i = 0; i < 50; i++)
	{
		score1 += Seed::score[dontCareRef[i]][dontCareQry[i]];
	}
	int32_t score2=0;
	for(uint32_t i = 50; i < 100; i++)
	{
		score2 += Seed::score[dontCareRef[i]][dontCareQry[i]];
	}
	if(score1>0&&score2>0)
		return score1+score2;
	else
		return -1;
}*/

int32_t Seed::getScore (std::vector<char> & dontCareRef, std::vector<char> & dontCareQry)
{
	int32_t score=0;
	for(uint32_t i = 0; i < dontCare; i++)
	{
		score += Seed::score[dontCareRef[i]][dontCareQry[i]];
	}
	return score;
}

void Seed::fillDontCare(std::vector<char> & vec, char * seq)
{
	for(uint32_t i = 0; i < dontCare; i++)
	{
		vec[i] = *(seq + dontCarePos[i]);
	}
}

void Seed::fillDontCareScore(std::vector<char> & vec, char * seq)
{
	for(uint32_t i = 0; i < dontCare; i++)
	{
		vec[i] = alphabet[ *(seq + dontCarePos[i]) ];

	}
}

void Seed::getFirstWord(unsigned char & w, char* seq)
{
		w |= alphabet[ *(seq + matchPos[0]) ] << 6;
		w |= alphabet[ *(seq + matchPos[1]) ] << 4;
		w |= alphabet[ *(seq + matchPos[2]) ] << 2;
		w |= alphabet[ *(seq + matchPos[3]) ];
}

void Seed::getNextWord(uint32_t & w, char* seq)
{
	uint32_t bits = (weight - 4) * 2 - 2;
	for(uint32_t i = 4; i < weight; i++)
	{
		w|=(uint32_t) alphabet[ *(seq + matchPos[i]) ] << bits;
		bits -= 2;
	}
}
