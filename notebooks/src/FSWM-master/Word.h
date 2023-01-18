#ifndef WORD_H_
#define WORD_H_

#include <stdlib.h>
#include <vector>
#include <string>
#include <iostream> 

class Word{
	private:
		int32_t pos;
		uint32_t key;
	public:
		Word(int32_t, uint32_t);

		uint32_t getKey();
		int32_t getPos();
		int32_t* getPosPointer();

		void setKey(uint32_t );

		bool operator<( const Word& val ) const { 
			return key < val.key; 
		}
};
#endif