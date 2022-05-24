import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                tag: "#81b4d2",
                primary: "#6a7fdb",
                secondary: "#13293d"
            }
        }
    }
});
