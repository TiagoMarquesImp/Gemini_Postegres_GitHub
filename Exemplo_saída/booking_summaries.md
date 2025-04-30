Okay, compreendido. Com base no esquema da tabela `booking_summaries` fornecido, aqui está o dicionário de dados em formato Markdown.

**Observação Importante:** O contexto do código Ruby on Rails (`{}`) estava vazio. Portanto, **não foi possível identificar ou explicar quaisquer `enums`** que possam estar definidos no model `BookingSummary`. Se houver `enums` associados a alguma coluna (por exemplo, um campo de status), por favor, forneça o código do model Rails para que eu possa incluí-los.

---

## Dicionário de Dados: Tabela `booking_summaries`

**Descrição da Tabela:** Armazena dados sumarizados sobre alocações ou reservas (bookings) de recursos em projetos para clientes, incluindo informações financeiras (taxas) e de horas trabalhadas/faturadas, agregadas por um período de competência.

| Coluna              | Tipo de Dados (PostgreSQL)   | Descrição                                                                                                | Restrições/Notas                                       |
| :------------------ | :--------------------------- | :------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| `id`                | `bigint`                     | Identificador único para cada registro de resumo de reserva.                                            | Chave Primária (PK), Não Nulo, Autoincremento (`nextval`) |
| `resource_id`       | `bigint`                     | Chave estrangeira (FK) referenciando a tabela de recursos (`resources`). Identifica o recurso alocado.      | Pode ser Nulo, FK (presumida para `resources.id`)      |
| `project_id`        | `bigint`                     | Chave estrangeira (FK) referenciando a tabela de projetos (`projects`). Identifica o projeto associado.     | Pode ser Nulo, FK (presumida para `projects.id`)       |
| `client_id`         | `bigint`                     | Chave estrangeira (FK) referenciando a tabela de clientes (`clients`). Identifica o cliente associado.      | Pode ser Nulo, FK (presumida para `clients.id`)        |
| `competency_date`   | `date`                       | Data de referência para o período de competência deste resumo (ex: primeiro dia do mês).                    | Não Nulo                                               |
| `billing_rate`      | `numeric`                    | Taxa/valor por hora cobrado do cliente pelo recurso neste período.                                        | Não Nulo                                               |
| `resource_rate`     | `numeric`                    | Taxa/valor por hora referente ao custo do recurso para a empresa neste período.                           | Não Nulo                                               |
| `created_at`        | `timestamp without time zone`| Data e hora em que o registro foi criado. Padrão do Rails.                                                 | Não Nulo                                               |
| `updated_at`        | `timestamp without time zone`| Data e hora da última atualização do registro. Padrão do Rails.                                            | Não Nulo                                               |
| `allocation_id`     | `bigint`                     | Chave estrangeira (FK) referenciando a tabela de alocações (`allocations`). Vincula o resumo a uma alocação. | Pode ser Nulo, FK (presumida para `allocations.id`)    |
| `resource_payment_id` | `bigint`                     | Chave estrangeira (FK) referenciando a tabela de pagamentos de recursos (`resource_payments`).             | Pode ser Nulo, FK (presumida para `resource_payments.id`)|
| `uuid`              | `uuid`                       | Identificador único universal para o registro, útil para integrações ou identificação externa.             | Pode ser Nulo                                          |
| `resource_hours`    | `numeric`                    | Número total de horas trabalhadas ou alocadas pelo recurso neste período de competência.                 | Pode ser Nulo                                          |
| `billing_hours`     | `numeric`                    | Número total de horas faturadas para o cliente neste período de competência.                             | Pode ser Nulo                                          |
| `base_hours`        | `numeric`                    | Número de horas base ou esperadas para o recurso no período (ex: horas úteis no mês).                     | Pode ser Nulo                                          |

---

Se você puder fornecer o conteúdo do arquivo do model Rails (`app/models/booking_summary.rb`), poderei atualizar este dicionário com as definições de `enum`, caso existam.