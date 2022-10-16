<template>
  <v-app>
    <div id="slogan">
      <div class="text-center">
        <div class="container">
        <div class="card-body">
          <h1>Hello World</h1>
          <div class="input-group">
            <!-- <input class="form-control" type="text" v-model="name" placeholder="Put Names Here"/> -->
            <v-text-field 
              v-model="name" 
              :rules="rules"
              counter="25"
              label="Name"
            ></v-text-field>
            <div class="input-group-append">
              <!-- <button class="btn btn-info" v-on:click="addNames(name)"></button> -->
              <v-btn
                depressed
                color="primary"
                v-on:click="addNames(name)"
              >
              Enter
              </v-btn>
            </div>
          </div>
        </div>
        </div>
        <div class="container" v-if="amount">
          <div class="row">
            <div class="col-md">
              <div class="card">
                  <!-- <ul class="list-group">
                    <li class="list-group-item" v-for="name in names" v-bind:key="name">
                      {{ name }}
                    </li>
                  </ul> -->
                <div class="card-body">
                  <v-list-item v-for="name in names" v-bind:key="name">
                      <v-list-item-content>
                        <v-list-item-title><router-link to="/about">
                          <v-btn
                            v-on:click="addNames2(name)"
                          >
                          {{name}}
                          </v-btn>
                        </router-link></v-list-item-title>
                        <v-divider></v-divider>
                      </v-list-item-content>
                  </v-list-item>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </v-app>
</template>

<script>
import "bootstrap/dist/css/bootstrap.css"
import "font-awesome/css/font-awesome.css"
let value = ''
let names = []
export default {
  name: 'App',
  data: function () {
    let condition = ''
    if(names.length != 0){
      condition = true
    }
    else{
      condition = false
    }
    return {
      names: names,
      amount: condition,
      rules: [v => v.length <= 25 || 'Max 25 characters']
    };
  },
  methods: {
    addNames(name){
      if(name.length <= 25){
        names.push(name);
        this.amount = true;
      }
    },
    addNames2(name){
      console.log("teste")
      value = name
    }
  }
};
export{ value }
</script>

<style>
#slogan{
  margin-top: 30px;
  margin-bottom: 30px;
}
</style>