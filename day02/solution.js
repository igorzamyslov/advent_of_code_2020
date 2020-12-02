import fs from 'fs';

function readInput() {
  return fs.readFileSync('./input.txt', {encoding: 'utf-8'});
}

function parseInput() {
  const input = readInput();
  const output = [];
  input.slice(0, -1).split('\n').forEach((line) => {
    const matches = line.match(/(\d+)-(\d+) (.): (.*)/);
    const [, firstDigit, secondDigit, letter, password] = matches;
    output.push([firstDigit, secondDigit, letter, password]);
  });
  return output;
}

function findAnswerPartOne() {
  let counter = 0;
  parseInput().forEach((input) => {
    const [from, to, letter, password] = input;
    const letterCount = password.split(letter).length - 1;
    if (letterCount >= from && letterCount <= to) {
      counter += 1;
    }
  });
  console.log('Part One Answer:', counter);
}

function findAnswerPartTwo() {
  let counter = 0;
  parseInput().forEach((input) => {
    let [firstIndex, secondIndex, letter, password] = input;
    // account for absence of 0-th index
    firstIndex = firstIndex - 1;
    secondIndex = secondIndex - 1;
    if ([password[firstIndex], password[secondIndex]].indexOf(letter) >= 0 &&
        password[firstIndex] !== password[secondIndex]) {
      counter += 1;
    }
  });
  console.log('Part Two Answer:', counter);
}

findAnswerPartOne();
findAnswerPartTwo();
