/*
 * WebMCP для пансионат-центр.рф (справочник по выбору пансионата).
 * Регистрирует три read-only инструмента для браузерных ИИ-агентов:
 *   1) search_articles — поиск статей по ключевым словам, категории и типу
 *   2) get_article_details — получить метаданные и краткое описание статьи
 *   3) get_contact_info — получить контакты и форму обратной связи
 * WebMCP — черновик стандарта для интеграции ИИ-агентов с веб-сайтами.
 * Если браузер не поддерживает WebMCP, скрипт молча ничего не делает.
 */
(function () {
  'use strict';

  // Получить контекст модели из браузера (если он поддерживает WebMCP)
  var mc = (typeof document !== 'undefined' && document.modelContext) ||
           (typeof navigator !== 'undefined' && navigator.modelContext);
  if (!mc) return; // WebMCP не поддерживается, выходим

  // Каталог статей (кэшируется в памяти браузера)
  var ARTICLES_CACHE = null;

  function text(value) {
    return {
      content: [
        {
          type: 'text',
          text: typeof value === 'string' ? value : JSON.stringify(value, null, 2)
        }
      ]
    };
  }

  function abs(path) {
    return new URL(path, location.href).href;
  }

  // Загрузить каталог статей из ai-catalog.json
  function loadArticles() {
    if (ARTICLES_CACHE) return Promise.resolve(ARTICLES_CACHE);

    return fetch(abs('ai-catalog.json'), { credentials: 'omit' })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (catalog) {
        var articles = [];
        if (catalog.categories && Array.isArray(catalog.categories)) {
          catalog.categories.forEach(function (cat) {
            if (Array.isArray(cat.articles)) {
              cat.articles.forEach(function (art) {
                articles.push({
                  slug: art.slug,
                  title: art.title,
                  url: art.url,
                  category: cat.title,
                  type: art.type || 'article',
                  keywords: art.keywords || []
                });
              });
            }
            if (Array.isArray(cat.regions)) {
              cat.regions.forEach(function (reg) {
                articles.push({
                  slug: reg.slug,
                  title: reg.name + ' — пансионат',
                  url: reg.url,
                  category: cat.title,
                  type: 'regional',
                  keywords: reg.keywords || []
                });
              });
            }
          });
        }
        ARTICLES_CACHE = articles;
        return articles;
      })
      .catch(function () {
        return [];
      });
  }

  // Инструмент 1: поиск статей
  var searchArticles = {
    name: 'search_articles',
    description: 'Поиск статей в справочнике по выбору пансионата. Можно искать по словам, фильтровать по категории и типу ухода. Возвращает до 10 статей с названиями, URL и краткой информацией.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Слова для поиска: «деменция», «лежачий», «договор», «Челябинск», «реабилитация» и т.д.'
        },
        category: {
          type: 'string',
          enum: [
            'Основные руководства',
            'Выбор по типам ухода',
            'Выбор по регионам',
            'Сравнение и выбор'
          ],
          description: 'Фильтр по категории справочника'
        },
        type: {
          type: 'string',
          enum: [
            'guide',
            'legal-guide',
            'safety-guide',
            'medical-guide',
            'financial-guide',
            'faq',
            'specialized',
            'regional',
            'comparison'
          ],
          description: 'Тип статьи'
        }
      }
    },
    annotations: {
      readOnlyHint: true
    },
    execute: function (input) {
      input = input || {};
      var query = String(input.query || '').toLowerCase();
      var category = String(input.category || '').toLowerCase();
      var type = String(input.type || '').toLowerCase();
      var words = query.split(/\s+/).filter(Boolean);

      return loadArticles().then(function (articles) {
        var found = articles.filter(function (art) {
          if (category && String(art.category).toLowerCase() !== category) return false;
          if (type && String(art.type).toLowerCase() !== type) return false;
          if (!query) return true;
          var hay = [art.title, (art.keywords || []).join(' ')].join(' ').toLowerCase();
          return words.every(function (w) { return hay.indexOf(w) !== -1; });
        }).slice(0, 10);

        if (found.length === 0) {
          return text('Статьи не найдены. Весь справочник: ' + abs(''));
        }

        var result = found.map(function (art) {
          return {
            title: art.title,
            url: art.url,
            category: art.category,
            slug: art.slug,
            keywords: art.keywords
          };
        });
        return text(result);
      });
    }
  };

  // Инструмент 2: получить метаданные статьи
  var getArticleDetails = {
    name: 'get_article_details',
    description: 'Получить метаданные одной статьи: название, URL, категорию, ключевые слова и тип. Идентификаторы (slug) можно получить через search_articles.',
    inputSchema: {
      type: 'object',
      properties: {
        slug: {
          type: 'string',
          description: 'Идентификатор статьи, например «kak-vybrat-pansionat» или «pansionat-dlya-lezhachih-bolnyh»'
        }
      },
      required: ['slug']
    },
    annotations: {
      readOnlyHint: true
    },
    execute: function (input) {
      var slug = String((input && input.slug) || '').toLowerCase().trim();
      return loadArticles().then(function (articles) {
        var art = articles.filter(function (a) { return a.slug === slug; })[0];
        if (!art) {
          return text('Статья «' + slug + '» не найдена.');
        }
        return text({
          slug: art.slug,
          title: art.title,
          url: art.url,
          category: art.category,
          type: art.type,
          keywords: art.keywords,
          openUrl: 'Откройте для чтения: ' + art.url
        });
      });
    }
  };

  // Инструмент 3: контакты и форма
  var getContactInfo = {
    name: 'get_contact_info',
    description: 'Получить контакты справочника для консультации, обратной связи и помощи в выборе пансионата.',
    inputSchema: {
      type: 'object',
      properties: {}
    },
    annotations: {
      readOnlyHint: true
    },
    execute: function () {
      return text({
        email: 'zames.78@mail.ru',
        contact_form_url: abs('kontakty/'),
        about_url: abs('o-sayte/'),
        privacy_policy_url: abs('politika/'),
        note: 'Для консультации по выбору пансионата заполните форму на странице контактов. Все данные конфиденциальны.',
        owner: 'Харитонов Матвей Васильевич (самозанятый)',
        disclaimer: 'Справочник предоставляет информационные материалы. Решение о выборе пансионата принимайте с участием врача, юриста и органов социальной защиты.'
      });
    }
  };

  // Массив инструментов
  var tools = [searchArticles, getArticleDetails, getContactInfo];

  // Попытаться зарегистрировать инструменты
  tools.forEach(function (tool) {
    try {
      if (typeof mc.registerTool === 'function') {
        var registration = mc.registerTool(tool);
        if (registration && typeof registration.catch === 'function') {
          registration.catch(function () {
            // Инструмент уже зарегистрирован или возникла ошибка — игнорируем
          });
        }
      }
    } catch (e) {
      // Политика браузера или другая причина — продолжаем
    }
  });

  // Альтернативный способ: если registerTool не поддерживается, используем provideContext
  if (typeof mc.registerTool !== 'function' && typeof mc.provideContext === 'function') {
    try {
      mc.provideContext({
        tools: tools,
        apiVersion: '0.1',
        provider: 'пансионат-центр.рф'
      });
    } catch (e) {
      // Провайдер контекста не поддерживается — ничего не делаем
    }
  }

  // Логирование (для отладки)
  if (typeof console !== 'undefined' && console.log) {
    console.log('📋 WebMCP для справочника инициализирован. Доступно', tools.length, 'инструментов.');
  }
})();