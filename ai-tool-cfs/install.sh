go mod tidy
go run generate.go
go build -o ai-tool main.go
rm ./privateKey && rm ./publicTable