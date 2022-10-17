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
      </v-list>
    </v-navigation-drawer>

   <div>
      <v-card style="margin-top: 10px; margin-left: 260px; margin-right: 10px;">
        <v-card-subtitle style="font-size: 14px;"> 
        <b>Alterações Respiratórias</b> 
        </v-card-subtitle>

        <v-divider></v-divider>

        <v-card-text>
          <v-form>
            <v-switch
              v-model="customizations.OVA"
              label="Obstrução de vias aéreas"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <br>
            Frequência Cardíaca (bpm):
            <br>
            <textarea
              v-model="customizations.DISP"
              color="orange darken-3"
              style="
              border-width: 2px 2px 2px 2px;
              border-style: solid;
              border-color: #000 #000 #000 #000;
              "
              
              hide-details
              @blur="getData()">
            </textarea>
            <v-switch
              v-model="customizations.FR"
              label="<= 10 IRPM"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.CIA"
              label="Cianose, enchimento capilar > 2s, com uso de musculatura acessória e SpO2 < 90 %"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.RAA1"
              label="Ruídos adventícios audíveis sem uso do estetoscópio"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.MVUA"
              label="Murmúrios vesiculares universalmente abolidos"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.ROVA"
              label="Risco de obstrução de vias aéreas"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.ER"
              label="Esforço respiratório com estridor, sialorréia, fala entrecortada"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.CAG"
              label="Crise de asma grave SpO2 > 90 a < 94%"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.RAA2"
              label="Ruídos adventícios audíveis com uso do estetoscópio"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.MVPA1"
              label="Murmúrios vesiculares parcialmente abolidos, associado a dispneia"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.HEM"
              label="Hemoptise (sangramento das vias aéreas baixas), com ou sem tosse"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.SAT1"
              label="Saturação SpO2 entre 90 a 94%, com frequência respiratória de 20 a 24 IRPM"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.TPEH"
              label="Tosse produtiva com escarros hemoptoicos ou com ruídos adventícios"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.MVPA2"
              label="Murmúrios vesiculares parcialmente abolidos sem dispneia"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.TP"
              label="Tosse produtiva"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.DGSI1"
              label="Dor de garganta com sinais de infecção"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.SAT2"
              label="Saturação SpO2 entre 90 a 94 %, assintomático"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.COR"
              label="Coriza"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.DGSI2"
              label="Dor de garganta sem sinais de infecção"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.TS"
              label="Tosse seca"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
            <v-switch
              v-model="customizations.SG"
              label="Sintomas gripais, sem febre"
              color="orange darken-3"
              
              hide-details
              @click="getData()"
            ></v-switch>
          </v-form>
      </v-card-text>
    </v-card> 
   </div>
  </v-app>
</template>

<script>
import axios from 'axios'

let API_HOST = 'http://localhost'
let API_PORT = '8000'

export default {
  mounted () {
    this.putClassificacao()
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
      customizations: {
          OVA: false,
          DISP: 80,
          FR: false,
          CIA: false,
          RAA1: false,
          MVUA: false,
          ROVA: false,
          ER: false,
          CAG: false,
          RAA2: false,
          MVPA1: false,
          HEM:  false,
          SAT1: false,
          TPEH: false,
          MVPA2: false,
          TP: false,
          DGSI1: false,
          SAT2: false,
          COR: false,
          DGSI2: false,
          TS: false,
          SG: false
      },
      risco: 5
    }
  },
  methods: {
    async getData(){
      this.risco = await this.getClassificacao()
    },
    async getClassificacao () {
        const paciente = this.customizations
        const paciente1 = {}
        for (var x in paciente){
            if (paciente[x] === false) {
                paciente1[x] = 0
            } else if (x === "DISP") {
              paciente1[x] = paciente[x]
            }
            else {
                paciente1[x] = 1
            }
        }
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/read?OVA=${paciente1.OVA}&DISP=${paciente1.DISP}&FR=${paciente1.FR}&CIA=${paciente1.CIA}&RAA1=${paciente1.RAA1}&MVUA=${paciente1.MVUA}&ROVA=${paciente1.ROVA}&ER=${paciente1.ER}&CAG=${paciente1.CAG}&RAA2=${paciente1.RAA2}&MVPA1=${paciente1.MVPA1}&HEM=${paciente1.HEM}&SAT1=${paciente1.SAT1}&TPEH=${paciente1.TPEH}&MVPA2=${paciente1.MVPA2}&TP=${paciente1.TP}&DGSI1=${paciente1.DGSI1}&SAT2=${paciente1.SAT2}&COR=${paciente1.COR}&DGSI2=${paciente1.DGSI2}&TS=${paciente1.TS}&SG=${paciente1.SG}`
        const response = await axios.get(url)
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
    putClassificacaoFig () {
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/gerar_fig`
        const response = axios.put(url)
        if (response == 0) {
            console.log("Error ao carregar dados!")
        }
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
</style>
