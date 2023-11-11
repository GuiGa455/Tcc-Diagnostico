<template>
  <v-app
    style="background: lightblue;"
    app
  >
    <v-navigation-drawer
      permanent
      :mini-variant="mini"
      width="250"
      app
    >
      <v-list
        dense
        class="py-0"
      >
        <v-list-item two-line>
          <v-list-item-content v-if="!mini">
            <h2 class="title" style="white-space: nowrap;">
              PRÉ DIAGNÓSTICO
            </h2>
          </v-list-item-content>

          <v-btn
            icon
            style="margin-left: -6px; margin-top: 15px; margin-bottom: 15px;"
            @click.stop="mini = !mini"
          >
            <v-icon color="#ff9800">
              {{ mini ? 'mdi-chevron-right' : 'mdi-chevron-left' }}
            </v-icon>
          </v-btn>
        </v-list-item>

        <v-divider></v-divider>

        <v-tooltip 
          right 
          :disabled="!mini" 
          v-for="item in items"
          :key="item.title"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-list-item
              :color="!item.disabled ? '#ff9800' : '#5d5d5d'"
              v-bind="attrs"
              v-on="on"
              :disabled="item.disabled"
            >
              <v-list-item-icon>
                <v-icon :small="item.small" :color="!item.disabled ? '#ff9800' : '#5d5d5d'">
                  {{ item.icon }}
                </v-icon>
              </v-list-item-icon>
            
              <v-list-item-content>
                <v-list-item-title color="#ff9800">
                  {{ item.title }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-tooltip>

        <v-divider></v-divider>

        <v-tooltip 
          right 
          :disabled="!mini" 
        >
          <template v-slot:activator="{ on, attrs }">
            <v-list-item
              :color="'#ff9800'"
              v-bind="attrs"
              v-on="on"
            >
              <v-list-item-icon>
                <v-icon :color="'#ff9800'">
                  mdi-arrow-left
                </v-icon>
              </v-list-item-icon>
            
              <v-list-item-content>
                <v-list-item-title color="#ff9800">
                  Back to portal
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>

        </v-tooltip>

        <v-tooltip 
          right 
          :disabled="!mini" 
        >
          <template v-slot:activator="{ on, attrs }">
            <v-list-item
              :color="'#ff9800'"
              v-bind="attrs"
              v-on="on"
            >
              <v-list-item-icon>
                <v-icon :color="'#ff9800'">
                  mdi-exit-to-app
                </v-icon>
              </v-list-item-icon>
            
              <v-list-item-content>
                <v-list-item-title color="#ff9800">
                  Logout
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>

        </v-tooltip>
        <v-divider></v-divider>

        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <h5 class="title2" style="white-space: nowrap; margin-left: 70px">
          CLASSIFICAÇÃO
        </h5>
        <br>
        <v-chip
          v-if="this.risco === 1"
          class="footer-chip"
          color="red"
          style="margin-left: 90px"
          x-large="true"
        >
          RED
        </v-chip>

        <v-chip
          v-if="this.risco === 2"
          class="footer-chip"
          color="orange"
          style="margin-left: 70px"
          x-large="true"
        >
          ORANGE
        </v-chip>

        <v-chip
          v-if="this.risco === 3"
          class="footer-chip"
          color="yellow"
          style="margin-left: 70px"
          x-large="true"
        >
          YELLOW
        </v-chip>

        <v-chip
          v-if="this.risco === 4"
          class="footer-chip"
          color="green"
          style="margin-left: 75px"
          x-large="true"
        >
          GREEN
        </v-chip>

        <v-chip
          v-if="this.risco === 5"
          class="footer-chip"
          color="blue"
          style="margin-left: 85px"
          x-large="true"
        >
          BLUE
        </v-chip>

        <br>
        <br>
        <div style="margin-left: 22%; margin-top: 50%">
        <doctor-view :customer="customizations" @rowClick="rowClick()"/>
        </div>
      </v-list>
    </v-navigation-drawer>

   <div>
      <v-card style="margin-top: 10px; margin-left: 260px; margin-right: 10px;">
        <v-card-subtitle style="font-size: 14px;"> 
        <b>Alterações Respiratórias</b> 
        </v-card-subtitle>

        <v-divider></v-divider>

        <v-card-text
            v-for="(value, key) in customizations"
            :key="key"
        >
          <v-form>
            <div v-if="((customizations[key] !== false) && (customizations[key] !== true)) && ((customizations[key] !== 0) && (customizations[key] !== 1))">
            <br>
                <strong>
                  {{ description[key][0] }}
                </strong>
            <br>
            {{ description[key][1] }}
            <br>
            <br>
            <textarea
              v-model="customizations[key]"
              color="orange darken-3"
              style="
              border-width: 2px 2px 2px 2px;
              border-style: solid;
              border-color: #000 #000 #000 #000;
              "
              
              hide-details
              @blur="getData()">
            </textarea>
            </div>
            <div v-else>
            <v-switch
                class="bold-label"
                :v-model="customizations[key]"
                :label="description[key][0]"
                color="orange darken-3"
                hide-details
                @click="getData(customizations[key], key)"
            ></v-switch>
            <div>
              {{ description[key][1] }}
            </div>
            </div>
          </v-form>
      </v-card-text>
    </v-card> 
   </div>
  </v-app>
</template>

<script>
import axios from 'axios'
import DoctorView from "./../components/DoctorView.vue"

let API_HOST = 'http://localhost'
let API_PORT = '8000'

export default {
  components: {
    DoctorView
  },
  mounted () {
    this.putClassificacao()
    this.getPacienteDefault()
    this.getNomeDescricaoSintoma()
  },
  data () {
    return {
        items: [
        { title: 'Alterações Respiratórias', icon: 'mdi-head-outline', small: false },
        ],
        mini: false,
        drawer: true,
        errorMsg: '',
        isProdEnvironment: 0,
        customizations: {},
        risco: undefined,
        description: {}
    }
  },
  methods: {
    async getData(data1=null, data2=null){
        if (data1 !== null && data2 !== null) {
            if (data1 === false) {
                this.customizations[data2] = true
            }
            else {
                this.customizations[data2] = false
            }
        }
        this.risco = await this.getClassificacao()
    },
    async getClassificacao () {
        const paciente = this.customizations
        const paciente1 = {}
        for (var x in paciente){
            if (paciente[x] === false) {
                paciente1[x] = 0
            } else if (x === "DISP") {
              paciente1[x] = parseInt(paciente[x])
            }
            else {
                paciente1[x] = 1
            }
        }
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/read`
        const response = await axios.put(url, paciente1)
        if (response.data == 0){
            console.log("Error ao carregar dados!")
        } else {
            return response.data
        }
    },
    putClassificacao () {
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/update`
        const response = axios.put(url)
        if (response == 0) {
            console.log("Error ao carregar dados!")
        }
    },
    async getPacienteDefault () {
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/paciente_default`
        const response = await axios.get(url)
        this.risco = response.data['RISCO']
        delete(response.data['RISCO'])
        let data = response.data
        for (const key in data) {
            if (data[key] === 0) {
                data[key] = false
            } else if (data[key] === 1) {
                data[key] = true
            }
        }
        this.customizations = data
    },

    async getNomeDescricaoSintoma () {
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/nome_descricao_sintoma`
        const response = await axios.get(url)
        this.description = response.data
    },

    putClassificacaoFig () {
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/gerar_fig`
        const response = axios.put(url)
        if (response == 0) {
            console.log("Error ao carregar dados!")
        }
    },
    rowClick () {
      window.location.reload(true);
    }
  }
}
</script>

<style>
  .title {
    color: #ff9800
  }
  .title2 {
    color: black;
  }
  .bold-label{
    font-weight: bold;
  }
</style>
