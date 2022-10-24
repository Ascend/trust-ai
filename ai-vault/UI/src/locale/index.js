import Vue from 'vue';
import VueI18n from 'vue-i18n';
import locale from 'element-ui/lib/locale';

Vue.use(VueI18n);

import zh from './lang/zh'
import en from './lang/en'

export const i18n = new VueI18n({
    locale: 'zh',
    messages: {
        zh,
        en
    },
    silentTranslationWarn: true
})

locale.i18n((key, value) => i18n.t(key, value));