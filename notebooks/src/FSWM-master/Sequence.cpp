#include "Sequence.h"

Sequence::Sequence(std::string header, std::string & seqLine)
{
	this->header = header;
	for (std::string::iterator it = seqLine.begin(); it != seqLine.end(); it++) 
	{	
		if(!std::isspace(*it))
		{
			char c = std::toupper(*it);
			if(c == 'A' || c == 'T' || c == 'G' || c == 'C')
				seq.push_back(c);
			//else
			//	seq.push_back('N');
		}
	}
	seqRev.reserve(seq.size());
	for (std::vector<char>::reverse_iterator rit = seq.rbegin(); rit != seq.rend(); rit++) 
	{
		switch(*rit)
		{
			case 'A': seqRev.push_back('T');break;
			case 'C': seqRev.push_back('G');break;
			case 'G': seqRev.push_back('C');break;
			case 'T': seqRev.push_back('A');break;
			case 'N': seqRev.push_back('N');break;
			default: exit(-1);
		}
	}
}

std::vector<Sequence> Sequence::read(std::string fileName)
{
	std::vector<Sequence> sequences;
	std::ifstream infile(fileName);
	std::string line;
	std::string header;
	std::getline(infile, line, '>');
	while (!infile.eof())
	{
		std::getline(infile, header);
		std::getline(infile, line, '>');
		sequences.push_back(Sequence(header, line));
    }
    return sequences;
}

void Sequence::sortFirstBits(Seed & s)
{
	wordCount = seq.size() - s.getLength() + 1;
	sortedWords.reserve(wordCount);
	std::vector<unsigned char> firstBits(wordCount,0);
	std::vector<uint32_t> prefixSum(MAX_BUCKETS,0);
	unsigned char w;
	for (int32_t i = 0; i < wordCount; i++)
	{
		unsigned char w=0;
		s.getFirstWord(w, &seq[i]);
		firstBits[i]=w;
	}

	for (int32_t i = 0; i < wordCount; i++)
		++prefixSum[(firstBits[i])];

	uint32_t t = 0;
  	for (uint32_t i = 0; i < MAX_BUCKETS; i++) 
  	{
  		std::swap(prefixSum[i], t);
  	  	t += prefixSum[i];
  	}

  	firstBuckets=prefixSum;
  	firstBuckets.push_back(wordCount);

  	for (int32_t i = 0; i < wordCount; i++) 
  	{
    	sortedWords[prefixSum[firstBits[i]]++] = Word(i,0);

  	}
}

void Sequence::sortFirstBitsRev(Seed & s)
{
	sortedWordsRev.reserve(wordCount);
	std::vector<unsigned char> firstBits(wordCount,0);
	std::vector<uint32_t> prefixSum(MAX_BUCKETS,0);
	unsigned char w;
	for (int32_t i = 0; i < wordCount; i++)
	{
		unsigned char w=0;
		s.getFirstWord(w, &seqRev[i]);
		firstBits[i]=w;
	}

	for (int32_t i = 0; i < wordCount; i++)
		++prefixSum[(firstBits[i])];

	uint32_t t = 0;
  	for (uint32_t i = 0; i < MAX_BUCKETS; i++) 
  	{
  		std::swap(prefixSum[i], t);
  	  	t += prefixSum[i];
  	}

  	firstBucketsRev=prefixSum;
  	firstBucketsRev.push_back(wordCount);

  	for (int32_t i = 0; i < wordCount; i++) 
  	{
    	sortedWordsRev[prefixSum[firstBits[i]]++] = Word(i,0);

  	}
}

void Sequence::sortNextBitsRev(Seed & s)
{
	#pragma omp parallel for schedule(dynamic)
	for(int32_t i = 1; i <= MAX_BUCKETS; i++)
	{
		for(int32_t j = firstBucketsRev[i-1]; j < firstBucketsRev[i]; j++ )
		{
			uint32_t w=0;
			s.getNextWord(w, &seqRev[sortedWordsRev[j].getPos()]);
			sortedWordsRev[j].setKey(w);
		}
		std::sort(sortedWordsRev.begin() + firstBucketsRev[i-1], sortedWordsRev.begin() + firstBucketsRev[i]);
	}
}

void Sequence::sortNextBits(Seed & s)
{
	#pragma omp parallel for schedule(dynamic)
	for(int32_t i = 1; i <= MAX_BUCKETS; i++)
	{
		for(int32_t j = firstBuckets[i-1]; j < firstBuckets[i]; j++ )
		{
			uint32_t w=0;
			s.getNextWord(w, &seq[sortedWords[j].getPos()]);
			sortedWords[j].setKey(w);
		}
		std::sort(sortedWords.begin() + firstBuckets[i-1], sortedWords.begin() + firstBuckets[i]);
	}
}

double Sequence::compareSequences(Sequence & qry, Seed & s, int threads, int threshold)
{
	std::vector<std::vector<uint32_t> >mismatches(threads,std::vector<uint32_t>(s.getDontCare()+1,0)); 
	std::vector<std::map<int32_t, int32_t> > scores(threads, std::map<int32_t, int32_t>() );
	#pragma omp parallel for schedule(runtime)
	for(int32_t i = 1; i <= MAX_BUCKETS; i++)
	{
		std::vector<char> dontCareRef(s.getDontCare());
		std::vector<char> dontCareQry(s.getDontCare());
		int tId=omp_get_thread_num();
		int32_t score;
		Bucket b(	sortedWords.begin() + firstBuckets[i-1], sortedWords.begin() + firstBuckets[i], qry.sortedWords.begin() + qry.firstBuckets[i-1], qry.sortedWords.begin() + qry.firstBuckets[i],
					qry.sortedWordsRev.begin() + qry.firstBucketsRev[i-1], qry.sortedWordsRev.begin() + qry.firstBucketsRev[i]);
		while(b.hasNext())
		{
			std::vector<MatchScore> matches;
			for(std::vector<Word>::iterator startS1 = b.getStartS1(); startS1 != b.getEndS1(); startS1++)
			{
				s.fillDontCareScore(dontCareRef, &seq[startS1->getPos()]);
				for(std::vector<Word>::iterator startS2 = b.getStartS2(); startS2 != b.getEndS2(); startS2++)
				{
					s.fillDontCareScore(dontCareQry, &qry.seq[startS2->getPos()]);
					score=s.getScore(dontCareRef, dontCareQry);
					//scores[tId][score]++;
					if(score>threshold)
					{	
						char mm=0;
						for(int j =0; j< dontCareRef.size(); j++)
							if(dontCareRef[j]!=dontCareQry[j])
								mm++;
						matches.push_back(MatchScore(startS1->getPos(), startS2->getPos(), score, mm));
					}
				}
				for(std::vector<Word>::iterator startS2Rev = b.getStartS2Rev(); startS2Rev != b.getEndS2Rev(); startS2Rev++)
				{
					s.fillDontCareScore(dontCareQry, &qry.seqRev[startS2Rev->getPos()]);
					score=s.getScore(dontCareRef, dontCareQry);
					//scores[tId][score]++;
					if(score>threshold)
					{
						char mm=0;
						for(int j =0; j< dontCareRef.size(); j++)
							if(dontCareRef[j]!=dontCareQry[j])
								mm++;
						matches.push_back(MatchScore(startS1->getPos(), startS2Rev->getPos(), score, mm));
					}
				}
			}
			std::sort(matches.begin(), matches.end());
			for(std::vector<MatchScore>::iterator m1 = matches.begin(); m1 != matches.end(); m1++)
			{
				if(m1->posS1 != -1 && m1->posS2 != -1 ){
					mismatches[tId][m1->mismatches]++;
					for(std::vector<MatchScore>::iterator m2 = (m1 + 1); m2 != matches.end(); m2++)
					{
						if(m2->posS1 == m1->posS1)
							m2->posS1 = -1;
						if(m2->posS2 == m1->posS2)
							m2->posS2 = -1;
					}
					m1->posS1 = -1;
					m1->posS2 = -1;
				}
			}
		}
	}

	/*for(int t = 1; t < threads;t++)
	{
		for(std::map<int32_t, int32_t>::iterator it = scores[t].begin(); it != scores[t].end(); it++)
		{
			scores[0][it->first]+=scores[t][it->second];
		}
	}
	for(std::map<int32_t, int32_t>::iterator it = scores[0].begin(); it != scores[0].end(); it++)
	{
			std::cout << it->first << " " <<  it->second << std::endl;
	}*/

	for(int t = 1; t < threads;t++)
	{
		for (int i=0; i< mismatches[0].size();i++)
		{
			mismatches[0][i]+=mismatches[t][i];
		}
	}
	double length=0;
	double mm=0;
	for (int i=0; i< mismatches[0].size();i++)
	{
		length += mismatches[0][i]*s.getDontCare();
		mm += mismatches[0][i]*i;
		//std::cout << i << " " <<  mismatches[0][i] << std::endl;
	}
	return -0.75*log(1.0-(4.0/3.0)*(mm/length));
}
