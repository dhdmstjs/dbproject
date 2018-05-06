<script>
import {Pie} from 'vue-chartjs'

export default {
  extends: Pie,
  props: ['chartData', 'optionsData'],
  data() {
    return {
    }
  },
  mounted () {
    console.log("chartData", this.chartData)
    console.log("optionsData", this.optionsData);
    this.renderChart( this.chartData, this.optionsData)
  }
}
</script>
