go mod tidy
go run generate.go
go build -o ai-whitebox main.go
rm ./privateKey && rm ./publicTable