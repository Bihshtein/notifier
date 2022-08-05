import unittest
from notification_manager import *
from entities import *


class TestNotifier(unittest.TestCase):
    def setUp(self) -> None:
        self.notifier = NotificationManager()
        self.uploaded_event = Event(
            start_date=datetime.now(),
            link='a',
            name='a',
            crawling_status=CRAWLING_STATUSES.TEXT_UPLOADED)

        self.crawled_event = Event(
            start_date=datetime.now(),
            link='a',
            name='a',
            crawling_status=CRAWLING_STATUSES.CRAWLING)

    def test_print_notifications(self):

        self.notifier.register_multi_entity(
            entity='CompanyForEvent', notification_target_property='event')

        self.notifier.register_crawlable_entity(
            entity='Event',
            notifyable_crawling_statuses=(CRAWLING_STATUSES.TEXT_UPLOADED,))

        company_for_event1 = CompanyForEvent(
            event=self.uploaded_event,
            company=Company(employees_min=1, employees_max=10, link='b', name='b'),
            is_deleted=False,
            is_blacklisted=False)

        deleted_company_for_event = CompanyForEvent(
            event=self.uploaded_event,
            company=Company(employees_min=1, employees_max=10, link='b', name='b'),
            is_deleted=True,
            is_blacklisted=False)

        self.notifier.notify(entity_obj=None, original_entity_obj=company_for_event1, entity_type='CompanyForEvent')
        self.notifier.notify(entity_obj=company_for_event1, original_entity_obj=None, entity_type='CompanyForEvent')
        self.notifier.notify(entity_obj=company_for_event1, original_entity_obj=deleted_company_for_event, entity_type='CompanyForEvent')
        self.notifier.notify(entity_obj=self.uploaded_event, original_entity_obj=self.crawled_event, entity_type='Event')

    def test_not_supported(self):

        self.assertRaises(Exception, self.notifier.notify, self.uploaded_event, self.crawled_event, 'Event')
        self.notifier.register_crawlable_entity(
            entity='Event',
            notifyable_crawling_statuses=(CRAWLING_STATUSES.TEXT_UPLOADED,))
        self.notifier.notify(entity_obj=self.uploaded_event, original_entity_obj=self.crawled_event,
                             entity_type='Event')
        self.assertRaises(Exception, self.notifier.notify, self.uploaded_event, self.crawled_event, 'Event2')

