Okay, especialista! Com base nas informações fornecidas, vamos gerar o dicionário de dados para a tabela `booking_occurrences`.

**Observação Importante sobre Enums:**

Você forneceu o schema do banco de dados, mas não o código do model Rails (`app/models/booking_occurrence.rb`, presumivelmente). A coluna `reason` (tipo `integer`) é quase certamente um `enum` definido nesse model. Sem o código do model, não consigo saber quais números correspondem a quais significados (ex: `0 => 'alocacao_normal'`, `1 => 'ajuste_horas'`, etc.).

**Incluirei um espaço reservado na descrição da coluna `reason` e explicarei como um enum funciona nesse contexto. Se você me fornecer o trecho relevante do model Rails que define o enum `reason`, posso atualizar o dicionário com os valores e significados exatos.**

---

## Dicionário de Dados - Tabela `booking_occurrences`

Esta tabela armazena ocorrências individuais ou eventos relacionados a uma reserva (booking), detalhando horas, motivos e outras informações pertinentes para cada evento específico dentro de um resumo de reserva maior.

| Nome da Coluna        | Tipo de Dados (PostgreSQL) | Nulável | Padrão                                           | Descrição                                                                                                                                                                                                                            |
| :-------------------- | :------------------------- | :------ | :----------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                  | `bigint`                   | Não     | `nextval('booking_occurrences_id_seq'::regclass)` | Identificador único da ocorrência de reserva (Chave Primária).                                                                                                                                                                     |
| `booking_summary_id`  | `bigint`                   | Sim     | `None`                                           | Chave estrangeira que referencia a tabela `booking_summaries` (assumindo o nome da tabela pai). Associa esta ocorrência a um resumo de reserva específico. Pode ser nulo dependendo da lógica de negócio (embora geralmente não seja). |
| `reason`              | `integer`                  | Não     | `None`                                           | Código inteiro que representa o motivo ou tipo desta ocorrência. **Este é um `enum` definido no model Rails `BookingOccurrence`.** Cada número inteiro mapeia para um significado específico (ex: 0 para 'Alocação Padrão', 1 para 'Ajuste', 2 para 'Cancelamento Parcial', etc.). **Necessito do código do model (`app/models/booking_occurrence.rb`) para detalhar os valores possíveis e seus significados.** |
| `resource_hours`      | `numeric`                  | Não     | `None`                                           | Quantidade de horas de *recurso* alocadas ou registradas nesta ocorrência específica. Pode representar o tempo que um recurso (pessoa, equipamento) esteve envolvido.                                                              |
| `billing_hours`       | `numeric`                  | Não     | `None`                                           | Quantidade de horas a serem *faturadas* para o cliente relacionadas a esta ocorrência. Pode ser igual ou diferente de `resource_hours` dependendo das regras de negócio.                                                    |
| `note`                | `text`                     | Sim     | `None`                                           | Campo de texto livre para adicionar notas, observações ou justificativas relevantes sobre esta ocorrência específica.                                                                                                              |
| `created_at`          | `timestamp without time zone` | Não     | `None`                                           | Data e hora em que o registro da ocorrência foi criado no sistema (padrão Rails).                                                                                                                                                  |
| `updated_at`          | `timestamp without time zone` | Não     | `None`                                           | Data e hora da última atualização do registro da ocorrência no sistema (padrão Rails).                                                                                                                                            |
| `competency_date`     | `date`                     | Sim     | `None`                                           | Data de competência da ocorrência. Utilizada para agrupar ou reportar ocorrências dentro de um período fiscal ou de faturamento específico (ex: Mês/Ano em que as horas devem ser consideradas).                                 |

---

**Próximos Passos:**

Para completar a descrição da coluna `reason`, por favor, forneça o conteúdo do arquivo do model Rails (`app/models/booking_occurrence.rb`), especificamente a parte onde o `enum` para `reason` é definido. Exemplo de como pode ser no model:

```ruby
# app/models/booking_occurrence.rb
class BookingOccurrence < ApplicationRecord
  belongs_to :booking_summary, optional: true # Exemplo de associação

  enum reason: {
    standard_allocation: 0,
    adjustment: 1,
    time_off: 2,
    overtime: 3
    # ... outros motivos
  }

  # ... resto do model
end
```

Com essa definição, poderei listar os valores (`standard_allocation`, `adjustment`, etc.) e seus correspondentes inteiros (0, 1, etc.) na descrição da coluna `reason`.