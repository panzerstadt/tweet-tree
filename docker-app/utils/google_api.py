# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import translate
# imports misc librarues
import six, os, re, sys, json


def detect_language_api(text, debug=False):
    """Detects the text's language.
    :returns ISO compatible language
    """
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    if debug:
        print('Text: {}'.format(text))
        print('Confidence: {}'.format(result['confidence']))
        print('Language: {}'.format(result['language']))
    return result


# sentiment of entire content
def analyze_sentiment(text='', explicit_credentials=True):
    """
    Detects the sentiment of the text
    https://cloud.google.com/natural-language/docs/analyzing-sentiment

    Detects sentiment in the document. You can also analyze HTML with:
    document.type == enums.Document.Type.HTML

    outpus score and magnitude
    The score of a document's sentiment indicates the overall emotion of a document.
    The magnitude of a document's sentiment indicates how much emotional content is present within the document,
    and this value is often proportional to the length of the document.

    TLDR:
    deifne your own threshold of what's strong emotion, then measure from there
    score = (- bad, + good, 0.0 either low emotion or mixed emotions)
    magnitude = (emotion / length of content) (how strong is the emotion in the content?)
    to find low emotions:
    if score = low, magnitude = low, emotion = low
    if score = low, magnitude = hight, emotion = mixed
    when comparing content of different length, use magnitude to normalize scores


    in relation to entity sentiment:
    magnitude is just every magnitude added together
    score is
    :param text:
    :param explicit_credentials:
    :return:
    """

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text,
        language='ja',
        type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    """
    It is important to note that the Natural Language API indicates differences between
    positive and negative emotion in a document, but does not identify specific positive and negative emotions.
    For example, "angry" and "sad" are both considered negative emotions. However, when the Natural Language API
    analyzes text that is considered "angry", or text that is considered "sad", the response only indicates that
    the sentiment in the text is negative, not "sad" or "angry".

    A document with a neutral score (around 0.0) may indicate a low-emotion document, or may indicate mixed emotions,
    with both high positive and negative values which cancel each out. Generally, you can use magnitude values to
    disambiguate these cases, as truly neutral documents will have a low magnitude value, while mixed documents
    will have higher magnitude values.

    When comparing documents to each other (especially documents of different length), make sure to use the
    magnitude values to calibrate your scores, as they can help you gauge the relevant amount of emotional content.
    """

    return sentiment


def analyze_entities_api(text=''):
    """
    ref: https://cloud.google.com/natural-language/docs/reference/rpc/google.cloud.language.v1#google.cloud.language.v1.AnalyzeEntitiesResponse
    name:
          The representative name for the entity.
    type:
          The entity type.
    metadata:
          Metadata associated with the entity.  Currently, Wikipedia
          URLs and Knowledge Graph MIDs are provided, if available. The
          associated keys are "wikipedia\_url" and "mid", respectively.
    salience:
          The salience score associated with the entity in the [0, 1.0]
          range.  The salience score for an entity provides information
          about the importance or centrality of that entity to the
          entire document text. Scores closer to 0 are less salient,
          while scores closer to 1.0 are highly salient.
    mentions:
          The mentions of this entity in the input document. The API
          currently supports proper noun mentions.
    sentiment:
          For calls to [AnalyzeEntitySentiment][] or if [AnnotateTextReq
          uest.Features.extract\_entity\_sentiment][google.cloud.languag
          e.v1.AnnotateTextRequest.Features.extract\_entity\_sentiment]
          is set to true, this field will contain the aggregate
          sentiment expressed for this entity in the provided document.

    :param document:
    :param verbose:
    :return: (entity.name, entity.type)
    """
    """Detects entities in the text."""

    client = language.LanguageServiceClient()

    print('analyzing entities for: {}'.format(text))

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    # TODO: specify only entities that we are interested in finding?
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    # is it a full name, or a common noun?
    entity_mention_type = ('TYPE_UNKNOWN', 'PROPER', 'COMMON')

    list_of_entities = []
    # todo: key entry by relevance or by entity name!?
    for entity in entities:
        list_of_entities.append({
            entity.name: {
                "entity salience": entity.salience,
                "entity type": entity_type[entity.type]
            }
        })
        #list_of_entities.append((entity.name, entity_type[entity.type], '{:.2f}'.format(entity.salience)))

    return list_of_entities


def analyze_entities(text=""):
    result = analyze_entities_api(text)

    output = []
    for r in result:
        for k, v in r.items():

            output.append({
                "label": k,
                "salience": v['entity salience'],
                "type": v['entity type']

            })
    return output


def analyze_entities_and_sentiment(text=""):
    sentiment = analyze_sentiment(text)
    entities = analyze_entities(text)

    try:
        magnitude = sentiment.magnitude
        score = sentiment.score
    except:
        magnitude = 0
        score = 0

    # [print(e)for e in entities]
    #
    # print(sentiment, type(sentiment))
    # print(entities, type(entities))

    output_dict = {
        "sentiment": {
            "magnitude": magnitude,
            "score": score
        },
        "entities": entities
    }

    return output_dict

if __name__ == "__main__":
    test_text = "But good procedural generation should give rise to emergent interestingness: fundamentally surprising and engaging dynamics that weren't explicitly placed there by a human designer. Genetic algorithms will give you that. Endless forms most beautiful..."
    r = analyze_entities_and_sentiment(test_text)

    print(json.dumps(r, indent=4, ensure_ascii=False))
