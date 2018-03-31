package main

import (
	"os"
	"bufio"
	"fmt"
	"sync"
	"crypto/sha256"
	"encoding/hex"
	"strings"
)

const CPUS = 8

func stringInSlice(a string, list *[]string) bool {
	for _, b := range *list {
		if b == a {
			return true
		}
	}
	return false
}

func getPasswords() (*[]string, *[]string) {
	fileHandle, _ := os.Open("data/hw3_ex2.txt")
	defer fileHandle.Close()
	fileScanner := bufio.NewScanner(fileHandle)

	var passwds []string
	var salts []string

	for i := 0; i < 22; i++ {
		fileScanner.Scan()
	}

	for i := 0; i < 10; i++ {
		fileScanner.Scan()
		parts := strings.Split(fileScanner.Text(), ",")
		salts = append(salts, parts[0])
		passwds = append(passwds, parts[1])
	}

	return &passwds, &salts
}

func getDictionary(path string) *[]string {
	fileHandle, _ := os.Open(path)
	defer fileHandle.Close()
	fileScanner := bufio.NewScanner(fileHandle)

	var dict []string

	for fileScanner.Scan() {
		dict = append(dict, fileScanner.Text())
	}

	return &dict
}

func testPasswords(batchSize int, start int, wg *sync.WaitGroup, dict *[]string, passwds *[]string, salts *[]string) {
	defer wg.Done()
	for i := start; i < start+batchSize || i < len(*dict); i++ {
		hasher := sha256.New()
		hasher.Write([]byte((*dict)[i]))
		hasher.Write([]byte((*salts)[i]))
		res := hex.EncodeToString(hasher.Sum(nil))
		if stringInSlice(res, passwds) {
			fmt.Println((*dict)[i])
		}
	}
	fmt.Println("Finished process starting at ", start)
}

func main() {
	fmt.Println("Getting passwords")
	passwds, salts := getPasswords()

	fmt.Println("Getting dictionary")
	dict := getDictionary("data/rockyou.txt")

	fmt.Println("Cracking...")
	siz := len(*dict)
	batchSize := siz / CPUS

	var wg sync.WaitGroup
	wg.Add(CPUS)

	for i := 0; i < CPUS; i++ {
		go testPasswords(batchSize, batchSize*i, &wg, dict, passwds, salts)
	}

	wg.Wait()
}
