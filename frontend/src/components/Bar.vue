<script>
import {Bar} from 'vue-chartjs'

export default {
  extends: Bar,
  props: ['chartData', 'optionsData'],
  data() {
    return {
    }
  },
  mounted () {
    this.renderChart( this.chartData, this.optionsData)
  }
}
</script>
