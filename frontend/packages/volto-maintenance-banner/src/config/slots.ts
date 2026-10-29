import type { ConfigType } from '@plone/registry';
import MaintenanceBanner from '../components/MaintenanceBanner/MaintenanceBanner';

export default function install(config: ConfigType) {
  config.registerSlotComponent({
    slot: 'aboveApp',
    name: 'MaintenanceBanner',
    component: MaintenanceBanner,
  });
  return config;
}
