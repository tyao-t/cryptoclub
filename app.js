const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const https = require("https");
const cors = require("cors");

var corsOptions = {
  origin: "http://localhost:4200"
};

const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://tyao_admin:rriveryth7@cluster-telus-ehs.4nek4.mongodb.net/hdb?retryWrites=true&w=majority',
{useNewUrlParser: true, useUnifiedTopology: true});

const Person = mongoose.model('Person', { name: String, email: String, phone: String});

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

app.use(express.static("public"))

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/signup.html");
})

app.post("/", (req, res) => {
    const dataShortcut = req.body;
    const name = dataShortcut.name;
    const phone = dataShortcut.phone;
    const email = dataShortcut.email;
    const p = new Person({name: name, email: email, phone: phone});
    p.save();
    res.sendFile(__dirname + "/success.html")
});

app.get("/data", (req, res) => {
    Person.find((err, foundPeople) => {
        //console.log(foundCats);
        res.send(foundPeople);
    });
})

app.post("/failure", (req,res) => {
    res.redirect("/");
});


app.listen(process.env.PORT ||  3000, () => {
    console.log("Server is running");
});

// f007cceda3aae0c781f67fa2f14f6713-us4
// 9660118054
