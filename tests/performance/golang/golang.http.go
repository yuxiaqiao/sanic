package main

import (
    "os"
    "net/http"
    "encoding/json"
    "github.com/gorilla/mux"
)

type Hello struct {
    Test      bool    `json:"test"`
}

func handler(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(Hello{Test:true})
}

func main() {
    router := mux.NewRouter().StrictSlash(true)
    router.HandleFunc("/", handler)

    //http.HandleFunc("/", handler)
    http.ListenAndServe(":" + os.Args[1], router)
}
