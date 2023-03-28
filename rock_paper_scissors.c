#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
int number_of_games = 3;
int const start_bucks = 100;
int grizz_bucks = start_bucks;
int comp_move;
int player_move;
int bet, results;
int games_played = 0;


int place_bet(int);
int comps_move();
int user_move();
int check_results(int, int, int);
int win_or_lose(int, int);
int play_again(int, int, int);
int count_games();

int main(){
do{
//Get Bet
 bet = place_bet(grizz_bucks);

//Update Total Grizz Bucks

//Get Moves
 player_move = user_move();
 comp_move = comps_move();

//Determine Who Wins or Loses

 results = win_or_lose(comp_move, player_move);

//Total Grizzbucks after bet
 grizz_bucks = check_results(grizz_bucks, bet, results);

//Play Again or Return Score
}
while(play_again(results, grizz_bucks, start_bucks) != 1);
 return 0;
}







int place_bet(int grizz_bucks1){

//Check if bet can be made
if(grizz_bucks1 <= 0){
 printf("You are out of GrizzBucks. Game Over :(\n");
	exit(0);
	return 0;
}

else{

//Get bet
 int bet, x;

 printf("You now have %d Grizzbucks. Enter the amound you would like to wager on the next game: ", grizz_bucks);
 do{
	x = scanf("%d", &bet);
	if (x != 1 || bet < 0){
		printf("Invalid Input! Enter the amount you would like to wager on the next game: ");
		while(getchar() != '\n');
	}
	else if(bet > grizz_bucks){
		printf("Insufficient Funds! Enter the amount you would like to wager on the next game: ");
	}
	else{
		break;
	}
}
while(1);
//subtract grizz bucks
//check if bet is a number

 return bet;

}
}




int user_move(){
 int player_move, comp_move;
 int valid_move = 0;

//Get User Move
 char move;

 printf("Great! Now enter your move (R)ock/(P)aper/(S)cissors : ");
do{
 scanf(" %c", &move);
 move = tolower(move);
 if(move == 'r'){
	player_move = 0;
	valid_move = 1;
}
 else if(move == 'p'){
	player_move = 1;
	valid_move = 1;
}
 else if (move == 's'){
	player_move = 2;
	valid_move = 1;
}
 else{
	printf("Please enter a valid move:\n");
}
}
while(valid_move == 0);
return player_move;
}
int comps_move(){
//Generate Computer Response
 comp_move = rand() % 3;
 return comp_move;
}



int win_or_lose(int comp1_move, int players_move) {
  // Define character arrays for player and computer moves
  char play_move[9];
  char comps_move[9];
  // Assign words to player moves
  if (players_move == 0) {
    strcpy(play_move, "Rock");
  } else if (players_move == 1) {
    strcpy(play_move, "Paper");
  } else {
    strcpy(play_move, "Scissors");
  }

  // Assign words to computer moves
  int array_size;
  if (comp1_move == 0) {
    strcpy(comps_move, "Rock");
    array_size = 4;
  } else if (comp1_move == 1) {
    strcpy(comps_move, "Paper");
    array_size = 5;
  } else {
    strcpy(comps_move, "Scissors");
    array_size = 8;
  }

  // Initialize variables for outcomes
  int outcome;

  // Determine outcome of game and update variables
 if (players_move == 0 && comp1_move == 2) {
    printf("You chose Rock, the computer has chosen Scissors. You Win!\n\n");
    outcome = 0;

 }
 else if (players_move == 1 && comp1_move == 0) {
    printf("You chose Paper, the computer has chosen Rock. You Win!\n\n");
    outcome = 0;

 }
 else if (players_move == 2 && comp1_move == 1) {
    printf("You chose Scissors, the computer has chosen Paper, You Win!\n\n");
    outcome = 0;
 }
 else if (players_move == comp1_move) {
    printf("You chose %s, the computer has chosen %s. You Tied.\n\n", play_move, comps_move);
    outcome = 2;
 }
 else {
    printf("You chose %s, the computer has chosen %s. You Lose!\n\n", play_move, comps_move);
    outcome = 1;
  }
  // Return outcome of game
  return outcome;
}

int check_results(int player_bucks, int player_bet, int results){
 if (results == 0){
	player_bucks += player_bet;
 }
 else if (results == 1){
	player_bucks -= player_bet;
 }
 else{
	return player_bucks;
 }
return player_bucks;
}

int play_again(int result,int current_bucks ,int starting_bucks){
int static wins = 0, ties = 0, losses = 0, total_winnings= 0;

 if (result == 0){
	wins++;
 }
 else if (result == 1){
	losses++;
 }
 else if (result == 2){
	ties++;
 }
 char play_game, x;
 int games_played = 0;
 int is_valid = 0;
 int lose, gain;
 games_played = wins + ties + losses;

 printf("Play Again? (Y/N): ");
do{
scanf(" %c", &play_game);
 printf("\n");
 x = tolower(play_game);
//Find total winnings or losings
 if (starting_bucks >= current_bucks){
	total_winnings = starting_bucks - current_bucks;
	lose=1;
}
 else if (starting_bucks <= current_bucks){
	total_winnings = current_bucks - starting_bucks;
	gain=1;
}
 if (x == 'y'){
	is_valid = 1;
	return 0;
 }
 else if (x == 'n'){
	is_valid = 1;
	printf("Sad to see you go! Here is your Summary:\n");
	printf("# of games played:   %d\n", games_played);
	printf("# of wins:           %d\n", wins);
	printf("# of losses:         %d\n", losses);
	printf("# of ties:           %d\n", ties);
	printf("Net Gain/Loss:       ");
}
 else{
	printf("Incorrect Choice! Play again? (Y/N): ");
 }
}
while(is_valid == 0);


//Paratheses if negative
	if(lose == 1){
		printf("(%d) Grizzbucks\n", total_winnings);
	}
	else if(gain == 1){
	printf("%d Grizzbucks\n", total_winnings);
	}
	exit(0);
}


