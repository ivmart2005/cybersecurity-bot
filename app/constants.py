from app.domain.models import Scenario, ScenarioType


SCENARIOS: list[Scenario] = [
    Scenario(
        type=ScenarioType.SCAM,
        topic="Звонок из банка по поводу операции",
        role="сотрудник банка",
        goal="убедить пользователя продиктовать код подтверждения",
    ),
    Scenario(
        type=ScenarioType.SCAM,
        topic="Сообщение от руководителя в мессенджере",
        role="руководитель компании",
        goal="попросить срочно перевести средства на указанные реквизиты",
    ),
    Scenario(
        type=ScenarioType.SCAM,
        topic="Покупатель на маркетплейсе просит оформить доставку",
        role="покупатель",
        goal="убедить перейти по ссылке для оформления доставки",
    ),
    Scenario(
        type=ScenarioType.SAFE,
        topic="Напоминание от поликлиники о записи к врачу",
        role="администратор поликлиники",
        goal="просто напомнить о приёме",
    ),
    Scenario(
        type=ScenarioType.SAFE,
        topic="Коллега просит прислать публичный документ по рабочему проекту",
        role="коллега по работе",
        goal="получить доступ к уже известному документу",
    ),
    Scenario(
        type=ScenarioType.SAFE,
        topic="Служба поддержки банка предлагает прийти в отделение для перевыпуска карты",
        role="сотрудник поддержки банка",
        goal="предложить личный визит в отделение",
    ),
]