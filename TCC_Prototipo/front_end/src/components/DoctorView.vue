<template >
  <div>
    <v-btn
      text
      rounded
      class="mr-4"
      color="secondary"
      outlined
      @click="init()"
    >
      <v-icon left dark> mdi-doctor </v-icon>
      MÉDICO
    </v-btn>

    <v-dialog
      v-model="dialog"
      width="490"
      content-class="gray-border rounded-xl elevation-24"
      persistent
    >
      <v-card style="padding: 15px; background-color: White">
        <div class="d-flex flex-column">
          <div class="d-flex">
            <v-card-title
              class="pa-0 me-auto"
              style="font-size: 20px"
            >
              PACIENTE / SINTOMAS
            </v-card-title>

            <v-icon
              @click="closeDialog()"
              color="orange"
            >
              mdi-close
            </v-icon>
          </div>

          <div class="pa-0 me-auto mt-10">
            Adicionar os dados do paciente atual no banco de dados:
          </div>

          <div class="mt-5 d-flex justify-center">
            <v-btn-toggle
              v-model="paciente"
              dense
              mandatory
              borderless
            >
              <v-btn :value="true" color="green">
                SIM
              </v-btn>
              <v-btn :value="false" color="red">
                NÃO
              </v-btn>
            </v-btn-toggle>
          </div>

          <div v-if="paciente">
            <div class="mt-5 d-flex justify-center">
              <v-btn-toggle
                v-model="risco"
                divided
                variant="outlined"
              >
                <v-btn :value="1">Vermelho</v-btn> 
                <v-btn :value="2">Laranja</v-btn>
                <v-btn :value="3">Amarelo</v-btn>
                <v-btn :value="4">Verde</v-btn>
                <v-btn :value="5">Azul</v-btn>
              </v-btn-toggle>
            </div>
          </div>

          <div class="pa-0 me-auto mt-10">
            Adicionar novo sintoma na plataforma:
          </div>

          <div class="mt-5 d-flex justify-center">
            <v-btn-toggle
              v-model="sintoma"
              dense
              mandatory
              borderless
            >
              <v-btn :value="true" color="green">
                SIM
              </v-btn>
              <v-btn :value="false" color="red">
                NÃO
              </v-btn>
            </v-btn-toggle>
          </div>

          <div v-if="sintoma">
            <div class="mt-5 d-flex justify-center">
              <v-text-field 
                v-model="nome_completo"
                color="white" 
                bg-color="white"
                label="Sintoma"
                variant="underlined"
              >
              </v-text-field>
            </div>

            <div class="d-flex justify-center">
              <v-text-field 
                v-model="sintoma_name"
                color="white" 
                bg-color="white"
                label="Sigla"
                variant="underlined"
              >
              </v-text-field>
            </div>

            <div class="d-flex justify-center">
              <v-text-field 
                v-model="descricao"
                color="white" 
                bg-color="white"
                label="Descrição"
                variant="underlined"
              >
              </v-text-field>
            </div>

            <div class="d-flex justify-center">
              <v-text-field 
                v-model="valor_inicial"
                color="white" 
                bg-color="white"
                label="Valor padrão"
                variant="underlined"
              >
              </v-text-field>
            </div>
          </div>

          <div class="mt-10 d-flex justify-center">
            <v-btn
              @click="updateData()"
              color = "orange"
            >
              SAVE
            </v-btn>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

let API_HOST = 'http://localhost'
let API_PORT = '8000'

export default {
  mounted() {
    this.selectedParity = this.parities[0].slice(0, 3);
  },
  data() {
    return {
        dialog: false,
        paciente: false,
        sintoma: false,
        sintoma_name: null,
        descricao: null,
        valor_inicial: null,
        risco: null,
        nome_completo: null
    };
  },
  props: ["customer"],
  methods: {
    closeDialog() {
        this.dialog = false
        this.paciente = false
        this.sintoma = false
        this.sintoma_name = null
        this.descricao = null
        this.valor_inicial = null
        this.risco = null
        this.nome_completo = null
    },
    postPaciente () {
      let data = this.customer
      for (const key in data) {
          if (data[key] === false) {
            data[key] = 0
          } else if (data[key] === true) {
            data[key] = 1
          } else {
            data[key] = parseInt(data[key])
          }
      }

      if (this.risco === null) {
        const url = `${API_HOST}:${API_PORT}/pre_classificacao/paciente`
        const response = axios.post(url, data)
        if (response == 0) {
            console.log("Error ao transferir dados do paciente!")
        }
        return
      }

      const url = `${API_HOST}:${API_PORT}/pre_classificacao/paciente?risco=${this.risco}`
      const response = axios.post(url, data)
      if (response == 0) {
          console.log("Error ao transferir dados do paciente!")
      }
    },
    postSintoma () {
      const url = `${API_HOST}:${API_PORT}/pre_classificacao/descricao?sintoma=${this.sintoma_name}&default=${this.valor_inicial}&nomecompleto=${this.nome_completo}&description=${this.descricao}`
        const response = axios.post(url)
        if (response == 0) {
            console.log("Error ao transferir dados do paciente!")
        }
    },
    updateData() {
      if (this.paciente && this.sintoma) {
        console.log("Não pode adicionar pacientes e sintomas ao mesmo tempo")
      } else {
        if (this.paciente) {
          this.postPaciente()
          this.$emit("rowClick")
        }
        if (this.sintoma) {
          this.postSintoma()
          this.$emit("rowClick")
        }
      }
      this.closeDialog()
    },
    init () {
      this.dialog = true
      console.log(this.customer)
    }
  },
};
</script>

<style lang="scss" scoped>
.border-dialog {
  border: 0.01em solid #ffa600c0 !important;
}
.box {
  display: flex;
  flex-wrap: wrap;
  align-items: center; /* applied in one line flex container */
}
.rfq-details-box-text {
  font-size: 16px;
}
.rfq-details-box-text-bold {
  font-weight: bold;
  font-size: 14px;
}
.price-box-title {
  font-size: 16px;
}
.price-box-bps {
  font-weight: bold;
  font-size: 34px;
}
.price-card-column {
  flex-direction: column;
  justify-content: center;
  width: 160px;
  padding: 15px 0px;
}
::v-deep .theme--dark.v-list-item .v-list-item__mask {
  color: unset !important;
  background: none !important;
}
.bounce {
  outline: 0;
  border-color: red !important;
  animation-name: bounce;
  animation-duration: 0.7s;
  animation-delay: 0.15s;
}
/* This approximates the ease-in-out-bounce animation from easings.net, which would require a plug-in to use*/
@keyframes bounce {
  0% {
    transform: translateX(0px);
    timing-function: ease-in;
  }
  37% {
    transform: translateX(5px);
    timing-function: ease-out;
  }
  55% {
    transform: translateX(-5px);
    timing-function: ease-in;
  }
  73% {
    transform: translateX(4px);
    timing-function: ease-out;
  }
  82% {
    transform: translateX(-4px);
    timing-function: ease-in;
  }
  91% {
    transform: translateX(2px);
    timing-function: ease-out;
  }
  96% {
    transform: translateX(-2px);
    timing-function: ease-in;
  }
  100% {
    transform: translateX(0px);
    timing-function: ease-in;
  }
}
.lock-price-border {
  border: 5px solid white;
}
.unlock-price-border {
  border: 5px solid #00a400;
}
.no-price-border {
  border: 5px solid #100e43;
}
.reject-price-border {
  border: 5px solid #f44336;
}
.cursor-pointer {
  cursor: pointer;
}
</style>