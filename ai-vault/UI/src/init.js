
import 'element-ui/lib/theme-chalk/index.css'
import './theme/theme/index.css'
import VueClipboard from 'vue-clipboard2'

import { 
  Tabs,
  TabPane,
  Input,
  Button,
  Icon,
  Table,
  TableColumn,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Dialog,
  Form,
  FormItem,
  Message,
  Row,
  Col,
  Pagination,
  Tooltip,
  Upload,
} from 'element-ui';

export function init(Vue) {
    Vue.prototype.$message = Message;

    Vue.use(VueClipboard)
    Vue.use(Tabs);
    Vue.use(TabPane);
    Vue.use(Input);
    Vue.use(Button);
    Vue.use(Icon);
    Vue.use(Table);
    Vue.use(TableColumn);
    Vue.use(Dropdown);
    Vue.use(DropdownMenu);
    Vue.use(DropdownItem);
    Vue.use(Dialog);
    Vue.use(Form);
    Vue.use(FormItem);
    Vue.use(Row);
    Vue.use(Col);
    Vue.use(Pagination);
    Vue.use(Tooltip);
    Vue.use(Upload);
  }