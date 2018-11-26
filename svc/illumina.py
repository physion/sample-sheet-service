import io

from sample_sheet import SampleSheet, Sample
from typing import List, Any, Dict, Mapping

SAMPLES = 'samples'
WORKFLOW_ACTIVITY = 'workflow_activity'
SOURCE_SAMPLE_STATE_ID = 'source_sample_state_id'
WORKFLOW_ACTIVITY_ID = 'workflow_activity_id'
WORKFLOW = 'workflow'
IDENTIFIER = 'identifier'
SAMPLE_STATES = 'sample_states'
CONTAINER_BARCODE_LABEL = 'container_barcode_label'
CONTAINER_POSITION = 'position'
ID = 'id'


def make_sample_sheet(body: Mapping[str, Any], adapter_result_type='adapter_barcode') -> str:
    wfa = body[WORKFLOW_ACTIVITY]
    activity_id = wfa[ID]
    wf = wfa[WORKFLOW]
    samples = wf[SAMPLES]

    sample_sheet = SampleSheet()
    for sample in samples:
        sample_sheet.add_samples(sample_records(activity_id, sample, adapter_result_type=adapter_result_type))

    return sample_sheet


def to_csv(sample_sheet: SampleSheet) -> str:
    with io.StringIO() as sio:
        sample_sheet.write(sio)
        return sio.getvalue()

def sample_records(activity_id: int, sample: Mapping[str,Any], adapter_result_type='adapter_barcode') -> List[Sample]:
    """
    Constructs a `sample_sheet.Sample` for each library adapter record for the sample.

    :param activity_id: Flow cell activity ID
    :param sample: Ovation sample JSON
    :param adapter_result_type: result type for library
    :return: List[sample_sheet.Sample]
    """
    adapter_results = sample_adapter_results(activity_id,
                                             sample,
                                             adapter_result_type=adapter_result_type)

    # req = sample['requisition']
    # panels = req['requested_tests']

    samples = []
    sample_identifier = sample[IDENTIFIER]
    for (_id, adapter_result_records) in adapter_results.items():
        sample_state = _sample_state_with_id(_id, sample[SAMPLE_STATES])
        for adapter_record in adapter_result_records:
            sample_attributes = dict(Sample_ID=to_sample_id(sample_identifier),
                                     Sample_Name=sample_identifier,
                                     Lane=position_to_lane(sample_state[CONTAINER_POSITION]),
                                     FCID=sample_state[CONTAINER_BARCODE_LABEL])

            sample_attributes.update(adapter_record)
            samples.append(Sample(**sample_attributes))

    return samples


def to_sample_id(sample_name: str) -> str:
    return sample_name.replace(' ', '_')[:100]  # 100 character max


def position_to_lane(container_position: str) -> int:
    return int(container_position[1:])


def sample_adapter_results(activity_id: int, sample: Mapping[str,Any], adapter_result_type='adapter_barcode') -> Dict[
    str, List[Dict[str, Any]]]:
    """
    Collects adapter WSR records for a sample. Traces backwards from flow cell activity to find the
    correct library WSR.

    :param activity_id: Flow cell activity ID
    :param sample: Ovation sample JSON
    :param adapter_result_type: result type for library
    :return: Map[sample_state_id,List[adapter_result_record]]
    """
    sample_states = sample[SAMPLE_STATES]

    activity_sample_states = [s for s in sample_states if s[WORKFLOW_ACTIVITY_ID] == activity_id]
    adapter_results = [r for r in sample['workflow_sample_results'] if r['result_type'] == adapter_result_type]

    adapter_result_workflow_activity_ids = [r[WORKFLOW_ACTIVITY_ID] for r in adapter_results]

    result = {}
    for s in activity_sample_states:
        records = []
        adapter_sample_state = _find_adapter_sample_state(s, sample_states, adapter_result_workflow_activity_ids)
        if adapter_sample_state:
            adapter_records = [r['result'][adapter_result_type]['records'] for r in adapter_results if
                               r[WORKFLOW_ACTIVITY_ID] == adapter_sample_state[WORKFLOW_ACTIVITY_ID]]
            for activity in adapter_records:
                for r in activity:
                    records.append(r)

        result[s[ID]] = records

    return result


def _find_adapter_sample_state(current_sample_state, sample_states, adapter_result_workflow_activity_ids):
    if current_sample_state[WORKFLOW_ACTIVITY_ID] in adapter_result_workflow_activity_ids:
        return current_sample_state

    if current_sample_state[SOURCE_SAMPLE_STATE_ID] is None:
        return None

    return _find_adapter_sample_state(
        _sample_state_with_id(current_sample_state[SOURCE_SAMPLE_STATE_ID], sample_states),
        sample_states,
        adapter_result_workflow_activity_ids)


def _sample_state_with_id(id, sample_states):
    for s in sample_states:
        if s['id'] == id:
            return s

    return None
