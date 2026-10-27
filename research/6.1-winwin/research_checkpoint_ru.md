# Structural complexity beyond ETH: research checkpoint

**27 октября 2026. Статус: доказательства ниже — исследовательские выводы, а не заявление о решении открытой проблемы.**

## 1. Главный результат и границы результата

Требуемая гипотеза с обеими полностью доказанными ветвями пока **не построена**. Получен существенный прогресс, меняющий выбор центрального объекта.

1. **Условный алгоритмический результат.** Если опубликованная теорема о детерминированном точном субэкспоненциальном #3SAT верна, то разреженная SCGS-CSP имеет рандомизированный алгоритм с односторонней ошибкой за `2^{o(N)} poly(|I|)`. Достаточен обычный целочисленный #SAT: weighted #SAT, поля характеристики два и предположение о компактной схеме ранга не нужны. Недостающее звено исходного репозитория — линейная изоляция, уже доступная в литературе.
2. **Более широкие следствия.** Для Connected Vertex Cover, Connected Dominating Set и невзвешенного Steiner Tree получается `2^{o(v)} poly(|I|)` даже на плотных графах. Для General CNF-SAT получается рандомизированная граница по `n+m`, а дополнительный интерполяционный аргумент даёт по этому же параметру детерминированный точный подсчёт. Это не граница только по числу переменных `n`.
3. **Структурный результат с настоящим circuit consequence.** Сатисфакция графового full-span с активациями только литералами, параметризованная числом свободных переключателей `p` отдельно от размера графа `S`, сохраняет исходные входы при кодировании polynomial-size branching programs. Детерминированный алгоритм `2^{o(p)} poly(S)` для этой задачи влечёт `NEXP not subseteq L/poly`. Элементарная width-five версия уже влечёт `NEXP not subseteq NC1`. Разделение `NEXP` и `P/poly` этим не получено.

**Критическое различие:** первый алгоритм рандомизирован. Он исключает соответствующую гипотезу трудности против рандомизированных алгоритмов, но сам по себе не опровергает детерминированную гипотезу. И второе: circuit consequence новой двухпараметрической гипотезы доказано, а её редукции **в** обычные HC/FVS/Set Cover с нужными параметрами пока отсутствуют.

Условные следствия новой #SAT-теоремы ниже помечены **[SAT26]**. Остальные элементарные леммы безусловны и используют явно названные стандартные результаты. Приоритет новизны не заявляется: новые здесь сочетания и доказательства требуют обычной независимой проверки.

## 2. Что проверено в источниках

На 27 октября доступны первичные материалы OpenAI и Anthropic. Объявлена внешняя проверка; завершённая независимая сертификация здесь не установлена. Lean-проект в этом сеансе не собирался.

В [OpenAI manuscript, Theorem 1.1](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf) заявлено для каждого фиксированного `k` точное #kSAT за

\[
(n+m)^{O_k(1)}2^{O_k(n\log\log n/\sqrt{\log n})}.
\]

При `m <= Dn`, фиксированном `D`, заявлен показатель `O_{k,D}(n/sqrt(log n))`. [Описание формализации](https://github.com/openai/math/blob/main/lean/docs/378.md) указывает более слабый показатель `O_k(n(log log n)^2/sqrt(log n))`; он также субэкспоненциальный. Область действия включает точный обычный подсчёт, а не автоматически произвольные веса. [Объявление и план проверки](https://openai.com/index/building-scientific-understanding-with-academic-communities/) следует читать отдельно от математического утверждения. Манускрипт уже содержит количественный lower bound для `E^NP` уровня infinitely-often `Omega(n sqrt(log n))`; его нельзя выдавать за новое следствие нашей гипотезы.

Независимый первичный набор — [Anthropic formal-math/eth](https://github.com/anthropics/formal-math/tree/main/eth), в частности [README](https://github.com/anthropics/formal-math/blob/main/eth/README.md) и [MainResults.lean](https://github.com/anthropics/formal-math/blob/main/eth/MainResults.lean). Его формальная оценка использует минимум выражений по числу клауз и переменных. Подробные оговорки об encoding, дубликатах и используемых переменных вынесены в сопровождающую записку `sat_status.md`.

Для главного алгоритмического вывода достаточно следующей явно условной предпосылки:

> **[SAT26]** Существует детерминированный точный #3SAT-алгоритм с временем `2^{o(q)} poly(L)` на `q` переменных и длине описания `L`, с заявленными выше количественными оценками, когда они используются.

Ключевой старый результат — [Applebaum, ECCC TR17-063, Theorem 2.3, Construction 4.4, Theorem 1.5](https://eccc.weizmann.ac.il/report/2017/063/download/): подходящие pairwise-independent hash functions имеют линейные схемы и дают полиномиально вычислимую локальную изоляцию с линейным увеличением числа переменных. Используем именно схему hash и однозначный Tseitin, без необходимости переносить counting через randomized encoding. Первоначальные конструкции хеширования обсуждаются также в [IKOS08, Theorem 3.3](https://web.cs.ucla.edu/~rafail/PUBLIC/91.pdf); для равномерности по длинам опираемся на формулировку и конструкцию Applebaum.

## 3. Параметры и формализм

Разделяем:

- `p` — число независимо выбираемых битов;
- `g` — размер bounded-fanin локальных схем и схем активации;
- `v,e` — вершины и рёбра графического описания матроида;
- `n,m,L` — переменные, клаузы и длина CNF;
- `u,t` — элементы универсума и число множеств в Set Cover;
- `q` — **все** переменные результирующего #SAT, включая свидетелей и gate variables;
- `N` — суммарное число объектов разреженной SCGS, `Theta(p+g+v+e)` с учётом локальных клауз;
- `S` — размер структурного описания в двухпараметрической модели; он может быть полиномом от `p`.

Списки рёбер и индексы обычно занимают `O(N log N)` бит. Поэтому `O(N)` здесь означает число объектов, а не буквально битовую длину. Все полиномиальные множители зависят от настоящего входа. Для матроидной прямой суммы размеры складываются.

SCGS использует графовые/кографические матроиды по явным графам, локальные Boolean gates с постоянным fanin и требование полного ранга. Auxiliaries детерминированных gates имеют **единственное** продолжение и входят в `q,N`. Мы не разрешаем бесплатно произвольную NP-проверку.

## 4. Лемма: линейная изоляция произвольного множества

**Утверждение.** Для `p>=1` можно за полиномиальное время случайно построить 3-CNF `H(x,a)` с `O(p)` дополнительными переменными и клаузами так, что:

1. каждому `x` соответствует не более одного удовлетворяющего `a`;
2. для **любого** непустого `A subseteq {0,1}^p` вероятность ровно одного продолжения с `x in A` не меньше `3/(16p)`;
3. построение не использует membership oracle для `A`.

**Доказательство.** Выбираем равномерно `s` из `{2,...,p+1}`. Берём из указанной теоремы линейную схему pairwise-independent семейства `h_w:{0,1}^p->{0,1}^s`, выбираем случайно key `w` и target `y`, фиксируем их как константы и кодируем `h_w(x)=y` через однозначный Tseitin. XOR и AND над `F_2` имеют постоянные Boolean реализации. Поэтому размер линейный, а gate values определены однозначно.

Пусть `K=|A|` и `s*=max(2,ceil(log_2 K)+1)`. Этот `s*` лежит в выбранном диапазоне, включая `K=1`. Для `Z=|A intersect h_w^{-1}(y)|` и `lambda=K/2^{s*}` имеем `1/4<=lambda<=1/2` и

\[
\mathbb EZ=\lambda,\qquad
\mathbb E[Z(Z-1)]=K(K-1)2^{-2s^*}\le\lambda^2.
\]

Для целого `z>=0` верно `1[z=1]>=z-z(z-1)`. Следовательно,

\[
\Pr[Z=1]\ge\lambda-\lambda^2\ge 3/16.
\]

Учитывая вероятность `1/p` выбора `s*`, получаем результат. При `p=0` проверяем единственный выбор напрямую. □

Исправление `max(2,...)` явно закрывает singleton endpoint. Случайный key фиксируется **до** подсчёта и не становится existential variable. Изолируются исходные решения `x`, а не будущие rank witnesses.

## 5. Общая теорема переноса parity в decision

Пусть fixed-width CNF `F(x,z)` имеет `q` переменных и для каждого `x`

\[
\#\{z:F(x,z)\}=\begin{cases}0,&x\text{ нарушает точные локальные условия},\\
2^{d(x)},&\text{иначе},\end{cases}
\]

где `d(x)>=0`, и настоящие решения — ровно локально допустимые `x` с `d(x)=0`.

**Теорема [SAT26].** Существование настоящего решения проверяется с односторонней ошибкой за `poly(p) T(q+O(p),poly(|I|))`, где `T` — время точного fixed-width #SAT. Для sparse формул с `q,#clauses=O(N)` получается заявленная граница

\[
\operatorname{poly}(|I|)2^{O(N/\sqrt{\log N})}.
\]

**Доказательство.** Добавим `H(x,a)` из предыдущей леммы. По единственности `a`

\[
\#(F\land H)\bmod2
=\#\{x:d(x)=0,\ x\text{ локально допустим и проходит }H\}\bmod2.
\]

При отсутствии решений результат всегда ноль. При наличии решений изоляция делает его единицей с вероятностью не меньше `3/(16p)`. За `O(p)` независимых повторений вероятность обнаружения превышает `2/3`; ошибочного YES не бывает. Добавлено `O(p)` переменных и клауз. Если для sparse оценки нужно обеспечить фиксированную плотность, можно добавить линейное число **зафиксированных** dummy bits с unit clauses. Свободные dummy bits недопустимы: они уничтожили бы чётность. □

После нечётного ответа можно получить свидетельство за `p` дополнительных parity queries: фиксируем очередной `x_i` в ноль, если соответствующий count нечётен, иначе в единицу. Сумма двух counts нечётна, поэтому инвариант сохраняется. Полученный `x` проверяем обычным вычислением ранга. Это даёт поиск на YES-инстансах; Las Vegas-решатель с завершением на NO из этого не следует.

## 6. Ранговые фильтры: полные доказательства

### 6.1. Бинарная матрица

Пусть `B` — full-row-rank бинарная матрица ранга `r`. Для активных столбцов `Y(x)` добавим `z in F_2^r` с условиями `B_Y^T z=0`. Размер kernel равен `2^{r-rank(B_Y)}`. Поэтому full-span отбирается чётностью. Каждый XOR вычисляется цепочкой gates с однозначными auxiliaries; размер `O(r+e+nnz(B))`, плюс активации. Если исходная матрица имеет зависимые строки, выбираем независимое подмножество **исходных** строк: row space сохраняется, а число ненулевых элементов не увеличивается.

Если разреженная матрица `D` представляет **двойственный** матроид, используем edge bits `z`, условия `Dz=0` и `z_e=0` при `e in Y`. При `Z=E\Y` число продолжений равно

\[
2^{|Z|-r_{M^*}(Z)}=2^{r_M(E)-r_M(Y)}.
\]

Равенство показателей — формула двойственного ранга. Следовательно, расширение модели до бинарных матроидов с разреженным primal **или dual** matrix description само по себе не спасает рандомизированную hardness hypothesis.

### 6.2. Графовый случай

Для каждого базового компонента `G` фиксируем одну вершину с меткой ноль. Остальным вершинам присваиваем witness bits `b_v`. Для каждого активного ребра `uv` требуем `b_u=b_v`.

В выбранном графе метка постоянна на каждом компоненте. Внутри каждого исходного компонента одна выбранная компонента закреплена, остальные свободны. Число меток поэтому

\[
2^{c(V,Y)-c(G)}=2^{r_{M(G)}(E)-r_{M(G)}(Y)}.
\]

Импликация `y_uv -> (b_u=b_v)` — две 3-клаузы. Имеем `v-c(G)` witness bits, `O(e)` клауз и стоимость локальных активаций. Этот подсчёт корректен при несвязном исходном графе; без anchors чётность была бы неверной даже при полном ранге.

### 6.3. Кографический случай

Берём по биту `z_e` на каждое ребро. На активированных рёбрах `Y` требуем `z_e=0`; в каждой вершине XOR инцидентных битов равен нулю. Получаем cycle space графа `(V,E\Y)` размерности `|E\Y|-v+c(V,E\Y)`. По двойственности это ровно дефицит cographic span.

Суммарная длина всех XOR — `2e`, поэтому после однозначного gate encoding требуется `O(v+e)` переменных и клауз. Петля учитывается дважды в incidence parity и остаётся свободной, как и положено циклу. Parallel edges допускаются. **Плотная cycle-space basis не строится.**

Для прямых сумм witness sets независимы, multiplicities перемножаются, а дефициты складываются. Теорема раздела 5 применима сразу ко всем компонентам.

### 6.4. Следствие для исходной SCGS

Для всех явно разреженных graphic/cographic direct sums с линейной local description получено `q=O(N)` и линейное число клауз. Поэтому **[SAT26]** даёт RP-вариант `2^{o(N)}`. Это закрывает именно вопрос «parity versus existence», оставленный открытым в исходном `docs/10_obstruction_parity_and_weighted_counting.md`.

Обычный подсчёт числа full-span решений этим не получен: точный count поднятой формулы включает чётные вклады невалидных решений. Отождествлять их нельзя.

## 7. Длинная клауза требует один parity bit

**Лемма.** Для произвольной клаузы `C=l_1 OR ... OR l_d` добавим один бит `t_C` и 2-клаузы

\[
(\neg t_C\lor\neg l_i)\quad(i=1,\ldots,d).
\]

При фиксированном `x` число продолжений — один, если `C` удовлетворена, и два, если нарушена.

**Доказательство.** `t_C=0` разрешён всегда. `t_C=1` разрешён ровно тогда, когда все `l_i` ложны. □

Для семейства клауз multiplicity равно `2^{#violated clauses}`. Пустая клауза даёт свободный бит, tautology принуждает бит к нулю. Это **не** обычная equisatisfiable-редукция: lifted формула может иметь решения при ложном `C`. Это точная parity-редукция, пригодная для раздела 5.

CNF на `n` переменных и `m` произвольных клаузах таким образом переводится в parity-2CNF на `n+m` переменных и `L` клаузах. После изоляции исходных `n` битов получаем **[SAT26]** RP-время `2^{o(n+m)} poly(L)`. В частности, случай `m=O(n)` больше не является подходящим кандидатом рандомизированной экспоненциальной трудности, даже при больших ширинах и числе вхождений.

Такие независимые фильтры можно перемножать с rank filters: общий показатель — сумма нарушений клауз и дефицитов ранга.

## 8. Плотная vertex connectivity на O(v) переменных

Нужен вариант, в котором большое `e` увеличивает число **клауз**, но не переменных. Пусть `s_v` выбирает непустое множество `U`, и фиксирован `r in U`. Введём два бита `a_v^0,a_v^1` на вершину с 3-CNF-условиями

\[
(\neg s_v\lor a_v^0\lor a_v^1),\quad
(s_v\lor\neg a_v^0),\quad(s_v\lor\neg a_v^1),\quad
(\neg a_v^0\lor\neg a_v^1).
\]

Следовательно, невыбранная вершина имеет состояние `(0,0)`, выбранная — ровно одно из `(1,0),(0,1)`. На каждом ребре `uv` добавим

\[
(\neg a_u^0\lor\neg a_v^1),\quad
(\neg a_u^1\lor\neg a_v^0).
\]

Фиксируем `s_r=1,a_r^0=1`. Тогда каждый компонент `G[U]` получает постоянную двухцветную witness label, компонент корня закреплён. Число продолжений **ровно** `2^{c(G[U])-1}`. Изолированные выбранные вершины считаются отдельными компонентами, а невыбранные не дают multiplicity. Все клаузы имеют ширину не больше трёх.

Unweighted cardinality `sum s_v<=k` имеет `O(v)` gates: carry-save compressors уменьшают число битовых элементов по одному за постоянную стоимость, всего `O(v)` раз; оставшиеся два слова длины `O(log v)` складываются и сравниваются. Значения всех gates однозначны.

**Следствия [SAT26], включая плотные графы.**

- **Connected Vertex Cover:** точные 2-клаузы `s_u OR s_v`, cardinality и этот connectivity filter. Пробуем все корни; пустой cover при отсутствии рёбер обрабатывается отдельно.
- **Connected Dominating Set:** по одной длинной клаузе `OR_{u in N[v]}s_u` на вершину; раздел 7 добавляет всего `v` witness bits. Добавляем cardinality и connectivity filter.
- **Unweighted Steiner Tree с edge budget k:** фиксируем terminal root, требуем все terminals в `U` и `|U|<=k+1`. Дерево с `k` рёбрами даёт такое множество; связное такое множество содержит spanning tree с не более чем `k` рёбрами. При отсутствии terminals — отдельный тривиальный случай.

Итого в каждом случае `q=O(v)`, `#clauses=O(v+e)`, максимум width 3; время

\[
\operatorname{poly}(v+e)2^{O(v\log\log v/\sqrt{\log v})}
\]

по общей заявленной #SAT-оценке. На sparse графах применима более сильная sparse оценка. Про weighted edge Steiner, параметр только по числу terminals и directed connectivity здесь ничего не утверждается.

## 9. Реестр естественных задач и размеров

| Задача | Доказанная связь / условное ускорение | Что остаётся непокрытым |
|---|---|---|
| HC | edge choices `p=e`; degree exactly 2 и graphic span; local size `O(v+e)`; RP `2^{o(v+e)}` | `2^{o(v)}` на произвольных плотных графах |
| FVS | `p=v`; удалённые рёбра активны в cographic matroid; rank witness `O(e)`; RP `2^{o(v+e)}` | `v`-only для плотных графов |
| General CNF-SAT | RP `2^{o(n+m)}` по одному clause bit; детерминированный exact count по тому же параметру ниже | только `n`, когда `m` существенно больше `n` |
| Set Cover | `t` choice bits, `u` coverage-filter bits, `O(t)` budget gates: RP `2^{o(t+u)}` даже при плотной incidence | только `u` при произвольном `t` |
| Fixed-k Coloring | `kv` one-hot bits, fixed-width clauses; deterministic `2^{o(v)}` при фиксированном k | Chromatic Number с растущим k |
| Connected VC / DS | раздел 8: RP `2^{o(v)}` на всех графах | детерминизация |
| Unweighted Steiner Tree | раздел 8: RP `2^{o(v)}` на всех графах | weighted edges / другой параметр |

Для HC degree exactly 2 кодируется линейным capped counter по incident bits, даже при большой степени. Поэтому bounded degree требуется только для `e=O(v)`, а не для самого кодирования. У FVS activation — OR удаления концов ребра; cardinality — линейный circuit. Формула двойственного ранга доказывает корректность для несвязных графов и не требует особого обещания связности.

В Set Cover coverage clauses имеют вид `OR_{j:u in A_j}x_j`. Лемма раздела 7 даёт один witness bit **на элемент**, без одной activation variable на каждую incidence. Это улучшает наивную star-кодировку по общему размеру incidences, но не устраняет `t` свободных битов. Линейное число множеств относительно `u` уже покрыто алгоритмом.

Отсутствие алгоритма в правом столбце означает отсутствие вывода **из проверенных здесь аргументов**, а не доказательство отсутствия новой статьи. Поиск не обнаружил надёжного первичного источника, закрывающего эти оставшиеся режимы.

## 10. Дополнительный deterministic counting результат: General #CNF по n+m

Этот результат не использует изоляцию. Его механизм — обычный block interpolation, см. [Curticapean, Block Interpolation: A Framework for Tight Exponential-Time Counting Complexity](https://arxiv.org/abs/1511.02910). Ниже дан полный специальный аргумент, включая веса, чтобы не предполагать weighted #SAT бесплатно.

**Лемма.** Exact #CNF на `n` переменных и `m` клаузах допускает **[SAT26]** детерминированный `2^{o(n+m)} poly(L)` алгоритм.

**Доказательство.** Построим граф. Для каждой переменной есть adjacent literal vertices `v_i^0,v_i^1` и special vertex `p_i`, смежная с обеими. Для каждой клаузы special vertex `c_j` смежна с literal vertices, удовлетворяющими её литералы. Special vertices независимы. Присвоим им activity `-1`, остальным activity 1.

Суммируем independent sets по выбранным literal vertices. Из пары можно выбрать не более одной. Если не выбрана ни одна, сумма по `p_i` равна `1+(-1)=0`. Иначе `p_i` запрещена. Следовательно, остаются ровно полные assignments. Аналогично `c_j` свободна с суммой ноль при нарушенной клаузе и запрещена при удовлетворённой. Weighted independent-set partition function равна **обычному** #CNF числу.

Теперь реализуем отрицательные activities через полиномиально описанные обычные counts. Разобьём `h=n+m` special vertices на `B=ceil(h/b)` блоков размера не больше `b`. Пусть `P(z_1,...,z_B)` — independent-set polynomial, где special vertices одного блока имеют activity `z_i`. Degree по каждой координате не больше `b`. Значение `P(-1,...,-1)` восстанавливается tensor-product Lagrange interpolation по сетке

\[
z_i\in\{2^j-1: j=0,\ldots,b\}.
\]

Для grid value `2^j-1` заменяем каждую соответствующую вершину `j` попарно несмежными false twins с теми же внешними соседями. Непустое подмножество twins выбирается `2^j-1` способами и имеет тот же внешний запрет. При `j=0` вершину удаляем. Каждая grid evaluation поэтому равна unweighted #IndependentSets в графе с `O(b(n+m))` вершинами. Это ровно #2SAT с одной переменной на вершину и клаузой `not x_u OR not x_v` на ребро.

Число запросов `(b+1)^{ceil(h/b)}`. Пусть `Q=n+m`, `b=max(1,floor(log_2(Q+2)^{1/4}))`. Общее заявленное время #2SAT и число запросов дают

\[
2^{O(Q\log\log Q/(\log Q)^{1/4})}\operatorname{poly}(L)=2^{o(Q)}\operatorname{poly}(L).
\]

Lagrange coefficients вычисляются точно рационально. Все одномерные знаменатели делят общий `D` с `log D=O(b^3)`. Tensor coefficients имеют общий знаменатель `D^B` с `O(Qb^2)` битами. Counts и числители также имеют полиномиальную битовую длину; интерполяцию можно выполнять как сумму grid counts с произведениями одномерных коэффициентов. Поэтому арифметика не скрывает дополнительной экспоненты. При использовании только более слабого формализованного #SAT-показателя аналогичный выбор всё ещё даёт `o(Q)`. □

В частности, обычный Dominating Set на плотных `v`-вершинных графах имеет CNF с `v` domination clauses плюс линейной cardinality-схемой и потому получает детерминированное субэкспоненциальное решение. Connected DS этим counting аргументом не детерминизируется: его connectivity filter всё ещё требует выделить дефицит ноль.

## 11. Лучшая текущая формулировка: Literal Graphic Span-SAT

**LGS(p,S).** Задан явный связный undirected multigraph `G` размера `S`. Каждое ребро помечено `0`, `1`, `x_i` или `not x_i`; `p` — число свободных switches. Для assignment активны рёбра с истинными метками. Вопрос: существует ли assignment, при котором активный граф связен, то есть spans `M(G)`? Локальных CSP-ограничений нет.

> **H_L.** Не существует детерминированного алгоритма LGS с временем `2^{o(p)} S^{O(1)}`, равномерно для polynomial-size descriptions `S=p^{O(1)}`.

Здесь матроидное условие существенно: вся проверка сводится к связности выбранного графа, а активация — один literal, без скрытой произвольной схемы. Параметр `S` нельзя подменять `p`. Это двухмасштабная гипотеза; она пока не является общей заменой ETH.

### 11.1. Линейная редукция branching programs в LGS

**Теорема.** Для ациклической deterministic branching program с `p` входными битами, размером `s` и двумя sinks `A` (accept), `R` (reject) существует LGS с теми же `p` битами и `S=O(s)`, причём для **каждого** `x`

\[
BP(x)=1\iff r_{M(G)}(Y(x))=r_{M(G)}(E).
\]

**Доказательство.** Каждую program vertex превращаем в графовую. Из внутреннего узла, читающего `x_i`, идут два направленных перехода; забываем направления, сохраняем рёбра как distinct edge objects и помечаем их `not x_i` и `x_i`. Для assignment из каждого внутреннего узла выбран ровно один переход. Добавим постоянно активное ребро `(start,R)` и постоянно неактивное ребро `(A,R)`.

До этих добавлений выбранный граф — лес с ровно двумя компонентами, корнями `A,R`. Действительно, следование единственному выбранному outgoing transition завершается в одном sink вследствие ацикличности. В одном undirected component все вершины имеют тот же конечный sink. Иначе на undirected path между разными sinks orientation потребовала бы вершину с двумя outgoing edges. Альтернативно, undirected cycle в acyclic orientation имел бы source с двумя outgoing edges, что также невозможно. Все vertices распределены между двумя деревьями.

Если program принимает, `start` лежит в компоненте `A`, и active edge `(start,R)` соединяет оба дерева. Если отвергает, ребро остаётся внутри компоненты `R`, и `A` отделена. Constant-zero edge `(A,R)` гарантирует связность **ground graph**, поэтому его rank — `|V|-1`. Связность selected graph теперь равносильна full-span. Число potential edges не больше двух на внутренний узел плюс два. Auxiliaries не введены. Start=sink и параллельные рёбра обрабатываются той же логикой. Для графового варианта петлю можно отбросить; для следующего кографического варианта сохраняем все edge identities. □

Та же редукция работает **кографически**: активируем в `M*(G)` дополнение выбранного forest-plus-edge множества `F_x+e`. Именно `F_x+e` имеет ровно `|V|-1` edge identities и является лесом ровно при accept. Двойственная формула ранга переводит это в cographic full-span; метки лишь инвертируются. При `start=R` добавленная петля обязательна: она и обеспечивает цикл в reject-случае.

Полиномиальные branching programs — модель `L/poly`. Обратно, LGS-предикат проверяется в `L/poly`: описание графа — advice, edge activation доступна в logarithmic space, а undirected connectivity находится в L по [Reingold](https://omereingold.wordpress.com/wp-content/uploads/2014/10/sl.pdf). То же верно для explicit cographic full-span через forest complement и для constant-arity локальных predicates без дополнительных свободных битов. Таким образом, polynomial-description literal graphic span — точная структурная модель `L/poly` на уровне предикатов. На уровне SAT это альтернативное графовое представление **BP-SAT**, и эту эквивалентность следует заявлять открыто. Про произвольные схемы `P/poly` здесь ничего не спрятано.

### 11.2. Точное следствие из отрицания H_L

**Теорема.**

\[
\neg H_L\quad\Longrightarrow\quad\mathrm{NEXP}\not\subseteq\mathrm{L/poly}.
\]

Уже только elementary width-five variant даёт `NEXP not subseteq NC1`. Для полного circuit target `P/poly` нужна дополнительная идея.

**Доказательство сильной формы.** Предполагаемый LGS-алгоритм и редукция раздела 11.1 дают deterministic BP-SAT за `2^{o(p)} poly(s)` для всех polynomial-size BP.

Используем easy-witness theorem: при `NEXP subseteq P/poly` принимающие экспоненциальные witnesses имеют polynomial-size circuit descriptions; точная формулировка — [Williams, Non-Uniform ACC Circuit Lower Bounds, Theorem 5.2](https://people.csail.mit.edu/rrw/acc-lbs.pdf). Предположим противное `NEXP subseteq L/poly`. Тогда выполнена и предпосылка easy-witness theorem, и `P subseteq L/poly`. Применение latter inclusion к Circuit Evaluation заменяет существующие polynomial-size witness circuits существующими polynomial-size BP (uniform compiler не требуется: BP будет guessed).

Выберем nondeterministic exponential-time language, запрещающий субэкспоненциальную nondeterministic simulation по time hierarchy. Для его входа длины `n` используем обычный регулярный Cook–Levin tableau размером `2^{O(n)}`. Клаузу такого tableau можно индексировать `O(n)` битами. Её тип и индексы переменных вычисляются в logarithmic space относительно длины индекса: нужны сравнения, соседние time/position indices и проверка фиксированного локального перехода. Input `x` хранится в описании; нужный входной символ выбирается сканированием. При необходимости стандартные constant-size gadgets дают 3CNF, не меняя `O(n)` бит индекса.

Нондетерминированно угадываем acyclic BP `W` фиксированного polynomial-size bound, выдающую assignment по индексу переменной tableau, и проверяем её синтаксис. Построим polynomial-size BP `D(z)`, проверяющую, нарушена ли индексированная клауза: вычисляем её не более чем три variable indices и трижды вызываем `W`. Logspace closure under composition обеспечивается повторным вычислением битов индекса; outer configuration хранится, inner evaluation использует ещё `O(log n)` space. Развёртка такой polynomial-time logspace проверки в явную BP полиномиальна.

Запускаем BP-SAT для `D` и принимаем guessed `W` ровно когда `D` unsatisfiable. Число независимых входов `D` — `O(n)`, поэтому время `2^{o(O(n))} poly(n)=2^{o(n)}`. При YES существует сжатый настоящий witness; при NO любой guessed `W` нарушает какую-либо клаузу, и deterministic SAT check это обнаруживает. Получена запрещённая nondeterministic subexponential simulation. Противоречие. □

Для слабых savings вместо subexponential premise нужен более экономный индекс `n+O(log n)` и точное применение стандартного Williams transfer; приведённое доказательство сознательно использует сильную `2^{o(p)}` предпосылку, где `O(n)` безопасно.

### 11.3. Независимая elementary NC1-проверка

[Barrington's theorem](https://doi.org/10.1016/0022-0000(89)90037-8) переводит depth-d fanin-two predicate в width-five permutation program длины не больше `4^d`, с product identity при false и fixed 5-cycle при true. Создадим пять вершин на каждом из `ell>=3` циклических layers. Инструкция активирует одно из двух matching permutations между соседними layers; рёбра имеют исходные literal labels. После обхода layers компоненты совпадают с orbits product permutation. Следовательно, false даёт пять компонент, true одну. Constant-zero spanning tree обеспечивает связность ground graph. Размер `O(4^d)`, свободных битов по-прежнему `p`.

При `d=O(log p)` размер полиномиален. Поэтому hypothetical LGS solver даёт `2^{o(p)} poly(size)` SAT для `NC1`. [Williams, Theorem 1.3](https://people.csail.mit.edu/rrw/acc-lbs.pdf) применим к `NC1` (содержит AC0 и замкнут относительно composition) и даёт `NEXP not subseteq NC1`. Этот независимый маршрут не использует reversible simulation и не зависит от обобщения circuit-model terminology на BP.

## 12. Почему P/poly-ветка пока не доказана

[Williams, Improving Exhaustive Search Implies Superpolynomial Lower Bounds, Theorem 1.1](https://people.csail.mit.edu/rrw/improved-algs-lbs2.pdf) требует настоящего ускорения SAT на `p` inputs и `p^k` gates для **всех** фиксированных `k`; достаточен deterministic/co-nondeterministic `2^p poly(p^k)/f(p)` с superpolynomial `f`. Его Theorem 1.2 из fixed fractional exponent saving для general Circuit-SAT получает exponential circuit lower bound в `E^NP`. Обычный bounded-error SAT не подставляется вместо этих предпосылок без отдельной теоремы. ETH-false consequence для linear circuits из Theorem 6.1 уже не является новым выигрышем.

Если бы всякий polynomial-size circuit predicate компилировался pointwise в polynomial-size literal/constant-arity (co)graphic span на **тех же** входах, то проверка результата в logspace дала бы

\[
\mathrm{P/poly}\subseteq\mathrm{L/poly}.
\]

Обратное включение стандартно, то есть получился бы collapse. Это условный structural barrier, не доказательство невозможности. Он не распространяется автоматически на SAT-only reductions, multi-instance reductions или использование новых existential bits. Последний обход возвращает проблему `p` против числа gates.

Есть и unconditional counting obstruction для **линейной** pointwise compression. Число explicit bounded-arity span descriptions из `O(p)` объектов — `2^{O(p log p)}`. Но уже функции от `floor(2 log_2 p)` первых входов дают `2^{Omega(p^2)}` разных predicates и все имеют circuits размера `O(p^2 log p)` через DNF. Поэтому все polynomial-size circuit predicates нельзя сохранить pointwise в `O(p)` объектов. Этот аргумент ничего не запрещает SAT-only reductions: они сохраняют лишь один answer bit.

`2^{o(p^k)}` не является `2^{o(p)}`. Более тонко, даже `N=p^{1+o(1)}` недостаточно для произвольного qualitative SUBEXP transfer: например, время `2^{N/log N}` при `N=p log^2 p` равно `2^{Theta(p log p)}`. Нужна конкретная скорость вместе с конкретным blow-up.

### 12.1. Более сильное препятствие: polynomial compression

Для полного LGS нельзя считать обычные polynomial-time reverse reductions просто ещё не найденными gadgets. Есть условный запрет, действующий **даже для SAT-only reductions**, в отличие от counting argument выше.

**Лемма.** Если LGS с `p` switches и произвольным polynomial-size description полиномиально сводится в обычный unweighted HC/FVS на `O(p)` вершинах, то `NP subseteq coNP/poly`. Более общо, не может быть одного такого reduction с output bit length `O(p^C)` при фиксированном `C` для всего семейства LGS, если `NP not subseteq coNP/poly`.

**Доказательство.** Любая `p`-переменная CNF вычисляется acyclic BP размера `O(L)`: последовательно сканируем literals клаузы, при истинном переходим к следующей клаузе, при исчерпании ложной клаузы — в reject. Accept после всех клауз. Для fixed d-SAT без повторов `L=O(p^d log p)`, так что source description полиномиален. Раздел 11.1 сохраняет ровно `p` switches. Предполагаемая reverse reduction сжимает ответ d-SAT до `O(p^C)` бит, где можно выбрать фиксированное `d>C`. Это запрещено [Dell–van Melkebeek, Theorem 1 / Corollary 1](https://people.csail.mit.edu/rrw/presentations/p251-dell.pdf) без указанного collapse. Для HC/FVS на `O(p)` вершинах достаточно adjacency matrix и budget, всего `O(p^2)` бит; уже `d=3` даёт противоречие. □

Это quantitative версия общего запрета SAT instance compression из [Fortnow–Santhanam](https://people.csail.mit.edu/rrw/presentations/fortnow-santhanam.pdf). Полиномиальное число коротких queries также ограничивается quantitative теоремой. Для Set Cover аналогичный вывод требует **фиксированной polynomial bound по p** на число множеств или на полный output length. Сам по себе universe `O(p)` при неограниченном числе множеств не обеспечивает короткий output.

Существование subexponential fixed-width SAT-алгоритма не противоречит этому барьеру: compression theorem требует polynomial-time preprocessing. Поэтому перспективный обход — **subexponential reduction families**, например время `2^{epsilon p} poly(S)` с параметром target `O_epsilon(p)` для каждого `epsilon>0`, или более узкий source. Ни новый входной параметр, ни заявленная новая SAT-теорема не отменяют этот запрет автоматически.

## 13. Три проверенные формулировки и их судьба

| Формулировка | Истинность | Ложность / алгоритмы | Вердикт |
|---|---|---|---|
| Sparse SCGS hardness против randomized `2^{o(N)}` | Давала бы hardness самой SCGS; для других targets нужны reverse reductions | **[SAT26]** плюс разделы 4–6 уже дают RP SUBEXP | Неподходящая основа при принятии #SAT26 |
| Sparse SCGS hardness против deterministic `2^{o(N)}` | Логически ещё возможна | Субэкспоненциальная local-SAT ветка не даёт нового P/poly consequence | Теперь в центре derandomization, не искомое общее комбинаторное препятствие |
| H_L: literal span, `p` switches / polynomial `S` | Hardness source для LGS/BP-SAT; обычные natural-target lower bounds пока не следуют | Доказано `NEXP not subseteq L/poly`; также elementary `NC1` consequence | Лучший текущий структурный кандидат с реальным falsity-side theorem, но полная win-win ещё открыта |

Кодировки HC/FVS/Set Cover **в** SCGS означают: быстрый SCGS-решатель ускоряет targets. Они не означают, что hardness SCGS доказывает hardness targets. В H_L нужно дополнительно учитывать, что число edge switches у HC равно `e`, а не `v`.

Объединение двух разных hardness assertions конъюнкцией не исправляет ситуацию: отрицание конъюнкции может дать лёгкость только той ветки, у которой нет нужного circuit consequence. Это логическая ошибка, а не источник win-win.

## 14. Компактные rank circuits

Для constructible fanin-two rank verifier размера `O(N log^alpha N)`, `alpha<1/2`, Tseitin даёт `q=O(N log^alpha N)`. Заявленный sparse #SAT exponent становится

\[
O(q/\sqrt{\log q})=O(N\log^{\alpha-1/2}N)=o(N).
\]

При использовании более слабой формализованной оценки появляется множитель `(log log N)^2`, который всё ещё поглощается `log^{1/2-alpha}N`. Поэтому количественный критерий корректен.

В проверенных источниках не установлена общая constructible схема такого размера для graphic/cographic rank. Из Reingold следует polynomial-size evaluation, но не нужный almost-linear gate bound. Линейное RAM time, polylog depth и маленькое пространство не равны gate size `O(N log^alpha N)`; стоимость адресации/слов и uniform construction нельзя пропускать. Также здесь не доказан circuit lower bound, запрещающий искомую схему.

Паритетный путь обходит этот вопрос для randomized existence: линейный **counting filter** не является линейным deterministic Boolean rank circuit. Поэтому результат раздела 6 не решает circuit-size задачу и не опровергает её возможность.

## 15. Что проверено вычислительно и что сохранено

`verify_checkpoint.py` — независимый stdlib-only verifier элементарных identities. Он перебирает small graphs/choices, считает ранг отдельным GF(2) elimination, independently enumerates cut/circulation witnesses, проверяет длинные клаузы, rooted connectivity и 3-state encoding. Дополнительно проверены direct BP-to-span, exact CNF cancellation, cycle-merging/ring gadgets и isolation moment estimate на малых affine hash families.

В `verification.json`: 760 graphic/cographic cases, 12 440 long-clause cases, 29 366 permutation cycle-merging cases, 446 ring/rank cases, 2 153 rooted/3-state connectivity cases, 18 exact probability cases, 12 144 BP/span cases и 819 exact CNF cancellation cases — все прошли. Эти эксперименты проверяют формулы и corner cases, **не** доказывают #SAT26, общий hash constructor, Williams theorem или asymptotic claims. Теоретические доказательства приведены выше.

Прочитаны README и релевантные docs исходного private repository; у веток A/E/G проверены деревья. По сравнению с main они не дали отдельной дополнительной реализации соответствующих центральных лемм. Исходная точка main: `4889bc8ccadd140bcb022866e9cf048b33e4accf`. Никакие synced `sources/` не изменены.

## 16. Следующие три математические задачи

1. **SERF вместо запрещённого polynomial compression.** Можно ли для каждого `epsilon>0` переводить LGS на `p` switches в `2^{epsilon p}` ordinary HC/FVS-инстансов с `O_epsilon(p)` вершинами, затрачивая `2^{epsilon p} poly(S)` времени? Это могло бы перенести hypothetical target SUBEXP обратно в LGS и дать truth-side hardness. Обычная polynomial-time reduction с теми же размерами упирается в раздел 12.1. Для universe-Set-Cover разрешить большой input length и явно учитывать число множеств.
2. **Детерминизация rank-filter algorithm.** Построить family из `2^{o(N)}` линейных hash restrictions, гарантирующую нечётный surviving count для любого непустого solution set именно rank/graph класса. Произвольные subsets автоматически не предполагаются. Альтернатива — иной deterministic способ извлечь coefficient rank-deficit zero из ordinary #SAT counts. Это конкретно отделяет детерминированный барьер от уже снятого рандомизированного.
3. **Переход за L/poly с input-efficient parameters.** Искать SAT-only, а не pointwise compilation из general Circuit-SAT в структурную модель с `p+o(p)` independent bits и polynomial description, либо расширить класс predicates за logspace так, чтобы не допустить бесплатной arbitrary verifier. Проверять каждую идею на collapse barrier раздела 12 и на точные Williams savings. Для sparse binary матриц сначала учитывать уже доказанный parity-filter collapse.

На этом checkpoint полноценная диаграмма «много классических lower bounds / NEXP против P/poly» остаётся открытой. Зато доказаны причины, по которым исходная sparse randomized гипотеза не годится, сокращён список живых задач и построен настоящий input-preserving графовый мост к сильному, хотя и ограниченному, circuit lower bound.
