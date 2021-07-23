from marshmallow import EXCLUDE, Schema, fields, pre_load, validate
from marshmallow_enum import EnumField

from src.paul.enums import NOC, Competition, League


class PredictionHeadersSchema(Schema):
    secret = fields.String(required=True)


class PredictionsRequestSchema(Schema):
    class Meta:
        ordered = True
        unknown = EXCLUDE

    _description = (
        "The key is a NOC and the value is the percentage of people that are "
        "considering this NOC as the winner for this medal "
    )

    @pre_load
    def map_dict_key_to_int(self, data, **kwargs):
        for field in ["gold", "silver", "bronze"]:
            if field in data and isinstance(data[field], dict):
                data[field] = {int(k): v for k, v in data[field].items()}

        return data

    gold = fields.Dict(
        keys=EnumField(
            NOC, by_value=True, error="Not a valid NOC (National Olympics Committees)"
        ),
        values=fields.Float(validate=validate.Range(min=0, max=1)),
        description=_description,
        example={"23": 0.512, "45": 0.1682, "146": 0.0798},
    )

    silver = fields.Dict(
        keys=EnumField(
            NOC, by_value=True, error="Not a valid NOC (National Olympics Committees)"
        ),
        values=fields.Float(validate=validate.Range(min=0, max=1)),
        description=_description,
        example={"23": 0.0012, "77": 0.76123, "81": 0.08921, "99": 0.001},
    )

    bronze = fields.Dict(
        keys=EnumField(
            NOC, by_value=True, error="Not a valid NOC (National Olympics Committees)"
        ),
        values=fields.Float(validate=validate.Range(min=0, max=1)),
        description=_description,
        example={
            "101": 0.09816,
            "1": 0.0013,
            "42": 0.81045103,
            "2": 0.0001,
            "3": 0.00005,
        },
    )


class PredictionRequestSchema(Schema):
    class Meta:
        ordered = True
        unknown = EXCLUDE

    test_mode = fields.Boolean(
        required=True,
        description="If true, it means that Paul is just testing if your code is OK. During the "
        "official prediction collection event, this will be set as false.",
    )

    league = EnumField(
        League,
        by_value=True,
        required=True,
        data_key="id_league",
        type="integer",
        description="A league is a set of players competing against each other. Full list: "
        "https://docs.google.com/spreadsheets/d/"
        "1RMdTBrka-ZNPfMNXZuMltxZbwD9MlHfUIcGFRprBo50",
        error="Invalid league",
    )

    competition = EnumField(
        Competition,
        by_value=True,
        required=True,
        data_key="id_competition",
        type="integer",
        description="Competition: 1 - Olympics; 2 - Paralympics",
        error="Invalid competition",
        example=1,
    )

    id_event = fields.Integer(
        required=True,
        description="Event: 1 - Cycling Road (M); 2 - Taekwondo (-58 kg) (M); Full list: "
        "https://docs.google.com/spreadsheets/d/"
        "1poZaLySfCtCPuRNWBne7plfJSNYyhx5yT9awViq-8uQ",
        example=1,
    )

    id_player = fields.Integer(
        required=True,
        description="Your player ID. You can use it to check security or you can just ignore it. "
        "To know your player ID, please send a message to the organization team.",
    )

    predictions = fields.Nested(
        PredictionsRequestSchema,
        required=False,
        default=None,
        description="2nd round only (if you win the coin-flip). It contains three maps: gold, "
        "silver and bronze. Each map has the NOC ID as the key (string formatted) and "
        "the percentage of people that are considering this NOC as the winner for "
        "this medal. Use this information to make a decision and return the same "
        "payload as in the first call. ",
    )


class PredictionResponseSchema(Schema):
    class Meta:
        ordered = True

    gold = EnumField(
        NOC,
        by_value=True,
        type="integer",
        description="Represents a NOC (National Olympics Committees)",
        example=NOC.BRAZIL.value,
    )

    silver = EnumField(
        NOC,
        by_value=True,
        type="integer",
        description="Represents a NOC (National Olympics Committees)",
        example=NOC.PEOPLES_REPUBLIC_OF_CHINA.value,
    )

    bronze = EnumField(
        NOC,
        by_value=True,
        type="integer",
        description="Represents a NOC (National Olympics Committees)",
        example=NOC.UNITED_STATES_OF_AMERICA.value,
    )
