from python_translators.translators.composite_parallel_translator import CompositeParallelTranslator

from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.factories.microsoft_translator_factory import MicrosoftTranslatorFactory
from python_translators.translation_caches.memory_cache import MemoryCache
from python_translators.translators.reverse_translator import ReverseTranslator
from python_translators.translators.duplicate_translator import DuplicateTranslator
from python_translators.translators.wordnik_translator import WordnikTranslator
from python_translators.config import get_key_from_config


class BestEffortTranslator(CompositeParallelTranslator):
    def __init__(self, source_language: str, target_language: str):
        super(BestEffortTranslator, self).__init__(source_language=source_language, target_language=target_language)

        lang_config = dict(
            source_language=source_language,
            target_language=target_language
        )

        if source_language == target_language == 'en':

            lang_config['key'] = get_key_from_config('WORDNIK_API_KEY')

            t = WordnikTranslator(**lang_config)
            t.quality = 90
            self.add_translator(t)

        else:
            google_translator_key = get_key_from_config('GOOGLE_TRANSLATE_API_KEY')
            microsoft_translator_key = get_key_from_config('MICROSOFT_TRANSLATE_API_KEY')

            if google_translator_key != "":

                # Google Translator WITH context
                t = GoogleTranslatorFactory.build_with_context(**lang_config)
                t.quality = 95
                self.add_translator(t)

                # Google Translator WITHOUT context
                t = GoogleTranslatorFactory.build_contextless(**lang_config)
                t.quality = 70
                self.add_translator(t)

            if microsoft_translator_key != "":

                # Microsoft Translator WITH context
                t = MicrosoftTranslatorFactory.build_with_context(**lang_config)
                t.quality = 80
                self.add_translator(t)
        
                # Microsoft Translator without context
                t = MicrosoftTranslatorFactory.build_contextless(**lang_config)
                t.quality = 60
                self.add_translator(t)
        

        self.set_cache(MemoryCache(translator_type='best_effort_translator'))


class DummyBestEffortTranslator(BestEffortTranslator):
    def __init__(self, source_language: str, target_language: str):
        # we don't want to call the direct super, but the one above that...
        super(BestEffortTranslator, self).__init__(source_language=source_language, target_language=target_language)

        lang_config = dict(
            source_language=source_language,
            target_language=target_language
        )

        # Google Translator with context
        t = ReverseTranslator(**lang_config)
        t.quality = 80
        self.add_translator(t)

        # Google Translator with context
        t = DuplicateTranslator(**lang_config)
        t.quality = 70
        self.add_translator(t)
