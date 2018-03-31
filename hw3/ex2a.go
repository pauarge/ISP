package main

import (
	"os"
	"bufio"
	"fmt"
	"sync"
	"crypto/sha256"
	"encoding/hex"
)

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func nextPassword(n int, c string) func() string {
	r := []rune(c)
	p := make([]rune, n)
	x := make([]int, len(p))
	return func() string {
		p := p[:len(x)]
		for i, xi := range x {
			p[i] = r[xi]
		}
		for i := len(x) - 1; i >= 0; i-- {
			x[i]++
			if x[i] < len(r) {
				break
			}
			x[i] = 0
			if i <= 0 {
				x = x[0:0]
				break
			}
		}
		return string(p)
	}
}

func testpasswords(n int, wg *sync.WaitGroup, passwds []string) {
	np := nextPassword(n, "abcdefghijklmnopqrstvuwxyz0123456789")
	for {
		pwd := np()
		if len(pwd) == 0 {
			break
		}
		hasher := sha256.New()
		hasher.Write([]byte(pwd))
		res := hex.EncodeToString(hasher.Sum(nil))
		if stringInSlice(res, passwds) {
			fmt.Println(pwd)
		}
	}
	wg.Done()
}

func main() {
	fileHandle, _ := os.Open("data/hw3_ex2.txt")
	defer fileHandle.Close()
	fileScanner := bufio.NewScanner(fileHandle)

	var wg sync.WaitGroup
	wg.Add(3)

	var passwds []string

	for i := 0; i < 11; i++ {
		fileScanner.Scan()
		passwds = append(passwds, fileScanner.Text())
	}

	go testpasswords(4, &wg, passwds)
	go testpasswords(5, &wg, passwds)
	go testpasswords(6, &wg, passwds)

	wg.Wait()

	fmt.Println("Done")
}
