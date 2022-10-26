import Vue from 'vue';
import VueI18n from 'vue-i18n';
import zhLocale from 'element-ui/lib/locale/lang/zh-CN';
import locale from 'element-ui/lib/locale';

Vue.use(VueI18n);

import zh from './lang/zh'
import en from './lang/en'

export const i18n = new VueI18n({
    locale: 'zh',
    messages: {
        zh: {
            ...zh,
            ...zhLocale,
          },
        en
    },
    silentTranslationWarn: true
})

locale.i18n((key, value) => i18n.t(key, value));
