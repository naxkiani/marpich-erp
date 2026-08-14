/**
 * Demo orchestrator — call Laboratory / Pharmacy public APIs with real peer patient IDs.
 * Hospital/Clinic never import peer domains; events → ACL → care-event projections.
 */
import type { ApiSession } from "./clientAuth";
import {
  finalizeLabResult,
  placeLabOrder,
  receiveLabSample,
} from "./laboratoryClient";
import { dispensePrescription, receivePrescription } from "./pharmacyClient";

export type CareEventSeedTarget = {
  patientId: string;
  encounterId?: string;
};

export type CareEventSeedResult = {
  labResults: number;
  dispenses: number;
  skipped: number;
  errors: string[];
};

function shortRef(id: string): string {
  return id.replace(/-/g, "").slice(0, 8).toUpperCase();
}

/**
 * For up to `maxPatients` targets: place lab order → sample → result, and Rx → dispense.
 * Default numbers are idempotent per patient (safe on reconnect).
 * Pass `uniqueKey` (e.g. timestamp) so a manual "Seed care events" can create fresh rows.
 */
export async function seedPeerCareEvents(
  session: ApiSession,
  targets: CareEventSeedTarget[],
  options: { maxPatients?: number; uniqueKey?: string } = {},
): Promise<CareEventSeedResult> {
  const maxPatients = options.maxPatients ?? 2;
  const suffix = options.uniqueKey ? `-${options.uniqueKey}` : "";
  const selected = targets.filter((t) => t.patientId).slice(0, maxPatients);
  const result: CareEventSeedResult = {
    labResults: 0,
    dispenses: 0,
    skipped: 0,
    errors: [],
  };

  for (const target of selected) {
    const tag = shortRef(target.patientId);
    const orderNumber = `CARE-${tag}-CBC${suffix}`;
    const accession = `ACC-${tag}${suffix}`;
    const rxNumber = `RX-CARE-${tag}${suffix}`;

    try {
      const order = await placeLabOrder(session, {
        order_number: orderNumber,
        patient_ref: target.patientId,
        test_code: "CBC",
        source_encounter_ref: target.encounterId,
      });
      await receiveLabSample(session, {
        order_id: order.id,
        accession_number: accession,
        specimen_type: "blood",
      });
      await finalizeLabResult(session, order.id, {
        result_value: "13.2",
        result_unit: "g/dL",
      });
      result.labResults += 1;
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      if (/order_number_exists|already|409|400/i.test(message)) {
        result.skipped += 1;
      } else {
        result.errors.push(`lab:${tag}:${message}`);
      }
    }

    try {
      const rx = await receivePrescription(session, {
        rx_number: rxNumber,
        patient_ref: target.patientId,
        drug_code: "AMOX500",
        drug_name: "Amoxicillin 500mg",
        quantity: 21,
        source_encounter_ref: target.encounterId,
      });
      await dispensePrescription(session, rx.id, 21);
      result.dispenses += 1;
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      if (/rx_number_exists|already|409|400/i.test(message)) {
        result.skipped += 1;
      } else {
        result.errors.push(`rx:${tag}:${message}`);
      }
    }
  }

  return result;
}

export function targetsFromPatientsAndEncounters(
  patients: Array<{ id: string }>,
  encounters: Array<{ id: string; patient_id: string }>,
): CareEventSeedTarget[] {
  return patients.map((p) => {
    const enc = encounters.find((e) => e.patient_id === p.id);
    return { patientId: p.id, encounterId: enc?.id };
  });
}

/** Prefer selected encounter; otherwise map patients → encounters (demo). */
export function targetsForCareEventSeed(
  patients: Array<{ id: string }>,
  encounters: Array<{ id: string; patient_id: string }>,
  selectedEncounterId?: string,
): CareEventSeedTarget[] {
  if (selectedEncounterId) {
    const enc = encounters.find((e) => e.id === selectedEncounterId);
    if (enc) {
      return [{ patientId: enc.patient_id, encounterId: enc.id }];
    }
  }
  return targetsFromPatientsAndEncounters(patients, encounters);
}
