from entities import *
from dataclasses import dataclass


@dataclass
class NotifcationSpecs:
    notification_target_property: str
    notifyable_properties: tuple[str]
    notifyable_crawling_statuses: tuple[CRAWLING_STATUSES]


class NotificationManager:

    def __init__(self):
        self.notifications_map = {}

    def register_crawlable_entity(self, *,
                                  entity: ENTITY_TYPES,
                                  notifyable_properties: tuple[str] = ('is_deleted',),
                                  notifyable_crawling_statuses: tuple[CRAWLING_STATUSES] = None):

        self._register_entity(
            entity=entity,
            notifyable_properties=notifyable_properties,
            notifyable_crawling_statuses=notifyable_crawling_statuses
        )

    def register_multi_entity(self, *,
                              notification_target_property : str,
                              entity: ENTITY_TYPES,
                              notifyable_properties: tuple[str] = ('is_deleted',),):

        self._register_entity(
            entity=entity,
            notification_target_property=notification_target_property,
            notifyable_properties=notifyable_properties,
        )

    def _register_entity(self, *,
                         notification_target_property: str = None,
                         entity: ENTITY_TYPES,
                         notifyable_crawling_statuses: tuple[CRAWLING_STATUSES] = None,
                         notifyable_properties: tuple[str] = ('is_deleted',)):
        self.notifications_map[entity] = NotifcationSpecs(
            notification_target_property=notification_target_property,
            notifyable_properties=notifyable_properties,
            notifyable_crawling_statuses=notifyable_crawling_statuses
        )

    def notify(self, *, entity_obj: object, original_entity_obj: object, entity_type: str):
        if entity_type in self.notifications_map:
            notification_specs = self.notifications_map[entity_type]

            if not entity_obj:
                self._send_notification_message(entity_obj=original_entity_obj, entity_type=entity_type)
            elif not original_entity_obj:
                self._send_notification_message(entity_obj=entity_obj, entity_type=entity_type)
            elif NotificationManager._lookup_crawling_status_changes(
                    notification_specs=notification_specs,
                    entity_obj=entity_obj,
                    original_entity_obj=original_entity_obj):
                self._send_notification_message(entity_obj=entity_obj, entity_type=entity_type)
            else:
                for notifyable_property in notification_specs.notifyable_properties:
                    if getattr(entity_obj, notifyable_property) != getattr(original_entity_obj, notifyable_property):
                        self._send_notification_message(entity_obj=entity_obj, entity_type=entity_type)
                        break
        else:
            raise Exception(f'the provided entity type ({entity_type}) is either not supported or not registered')

    @staticmethod
    def _lookup_crawling_status_changes(*, notification_specs, entity_obj, original_entity_obj):
        return notification_specs.notifyable_crawling_statuses and \
            getattr(entity_obj, 'crawling_status') in notification_specs.notifyable_crawling_statuses and \
            getattr(entity_obj, 'crawling_status') != getattr(original_entity_obj, 'crawling_status')

    def _send_notification_message(self, *, entity_obj: object, entity_type: str):
        if self.notifications_map[entity_type].notification_target_property:
            notify_on_property = self.notifications_map[entity_type].notification_target_property
            print(f'notify on {getattr(entity_obj, notify_on_property)}')
        else:
            print(f'notify on {entity_obj}')
